# from django.db import models

# from django.contrib.auth.models import User

# class Message(models.Model):
#     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
#     room = models.CharField(max_length=255, default='public')

#     def __str__(self):
#         return f"{'Admin' if self.is_admin else 'User'}: {self.content[:20]}"
    
    
# # from django.contrib.auth import get_user_model

# # User = get_user_model()

# # class ChatRoom(models.Model):
# #     shipment = models.OneToOneField('app.Shipment', on_delete=models.CASCADE, related_name='chat_room')
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return f"Chat for Shipment {self.shipment.tracking_id}"

# # class Message(models.Model):
# #     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
# #     sender = models.ForeignKey(User, on_delete=models.CASCADE)
# #     content = models.TextField()
# #     timestamp = models.DateTimeField(auto_now_add=True)
# #     read = models.BooleanField(default=False)

# #     class Meta:
# #         ordering = ['timestamp']

# #     def __str__(self):
# #         return f"Message from {self.sender.email} at {self.timestamp}"


# chat/models.py
from django.db import models

class ChatSession(models.Model):
    email = models.EmailField()  # Visitor's email for the chat session
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.id} ({self.email})"

class Message(models.Model):
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    sender = models.CharField(max_length=60, choices=[('visitor', 'Visitor'), ('admin', 'Admin')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Show sender and first 20 chars of content for identification
        return f"{self.sender.capitalize()} message in Session {self.chat.id}: {self.content[:20]}"


