# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import ChatRoom, Message
# from .serializers import ChatRoomSerializer, MessageSerializer

# class ChatRoomDetail(generics.RetrieveAPIView):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         shipment_id = self.kwargs['shipment_id']
#         return ChatRoom.objects.get(shipment_id=shipment_id)

# class MessageList(generics.ListCreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         shipment_id = self.kwargs['shipment_id']
#         room = ChatRoom.objects.get(shipment_id=shipment_id)
#         return Message.objects.filter(room=room).order_by('timestamp')

#     def perform_create(self, serializer):
#         shipment_id = self.kwargs['shipment_id']
#         room = ChatRoom.objects.get(shipment_id=shipment_id)
#         serializer.save(room=room, sender=self.request.user)


# chat/views.py
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, Message
from django.core.mail import send_mail

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def messages_api(request):
    print("API TEST")
    # Allow preflight OPTIONS request for CORS
    if request.method == "OPTIONS":
        response = HttpResponse(status=200)
        response["Access-Control-Allow-Origin"] = "*"  # allow all domains for simplicity
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == "POST":
        # Handle a new message from visitor (possibly starting a new session)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        email = data.get("email")
        session_id = data.get("session_id")
        content = data.get("content")
        if not content:
            return JsonResponse({"error": "Empty message content"}, status=400)

        
        # If no session_id provided, create a new ChatSession (requires an email)
        if not session_id:
            if not email:
                return JsonResponse({"error": "Email is required for new session"}, status=400)
            session = ChatSession.objects.create(email=email)
        else:
            try:
                session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                return JsonResponse({"error": "Invalid session"}, status=404)

        # Save the visitor's message
        msg = Message.objects.create(chat=session, sender='visitor', content=content)

        logger.info(f"Message received from {session.email}. Notified? {session.notified}")

        if not session.notified:
            logger.info("Sending notification email...")

            try:
                send_mail(
                    subject="New Chat Message from Website",
                    message=f"New message from {session.email}:\n\n{content}",
                    from_email=session.email,
                    recipient_list=["globaldeliveryeco@gmail.com"],
                    fail_silently=False,
                )
                session.notified = True
                session.save()
                logger.info("Email sent successfully.")
            except Exception as e:
                logger.error(f"Email sending failed: {e}")

        response_data = {
            "session_id": session.id,
            "admin_display_name": session.admin_display_name,
            "message_id": msg.id,
            "timestamp": msg.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        response = JsonResponse(response_data)
        response["Access-Control-Allow-Origin"] = "*"  # allow cross-site
        return response

    elif request.method == "GET":
        # Handle polling for new messages
        session_id = request.GET.get("session_id")
        last_id = request.GET.get("last_id")  # ID of last message already seen by visitor
        if not session_id:
            return JsonResponse({"error": "session_id required"}, status=400)
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Invalid session"}, status=404)
        # Query messages for this session. If last_id is provided, get messages with greater IDs (newer messages).
        msgs_query = Message.objects.filter(chat=session)
        if last_id:
            try:
                last_id = int(last_id)
                msgs_query = msgs_query.filter(id__gt=last_id)
            except ValueError:
                pass  # if last_id is not an integer, ignore it
        msgs_query = msgs_query.order_by("id")

        # Prepare list of message data to return
        messages_data = []
        for m in msgs_query:
            messages_data.append({
                "id": m.id,
                "sender": m.sender,
                "content": m.content,
                "timestamp": m.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
        response = JsonResponse({"messages": messages_data, "admin_display_name": session.admin_display_name or "Support Agent"})
        response["Access-Control-Allow-Origin"] = "*"
        return response

    else:
        # Method not allowed
        return JsonResponse({"error": "Method not allowed"}, status=405)
