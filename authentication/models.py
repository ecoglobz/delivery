from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, default='admin')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def update_login_info(self, ip_address):
        self.last_login_ip = ip_address
        self.last_login_time = timezone.now()
        self.save()

class LoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{status} login attempt by {self.username} from {self.ip_address} at {self.timestamp}"
