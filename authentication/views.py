from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializer import UserSerializer, LoginSerializer, ChangePasswordSerializer
from .models import LoginAttempt, UserProfile

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        ip_address = get_client_ip(request)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Create or update user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.update_login_info(ip_address)
            
            # Log successful login attempt
            LoginAttempt.objects.create(
                username=user.username,
                ip_address=ip_address,
                success=True
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        # Log failed login attempt
        LoginAttempt.objects.create(
            username=request.data.get('username', ''),
            ip_address=ip_address,
            success=False
        )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            # In a more complete implementation, you might want to blacklist the token
            return Response({"detail": "Successfully logged out."})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"detail": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({"detail": "Password updated successfully."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
