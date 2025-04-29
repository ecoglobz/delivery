from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    shipment = models.OneToOneField('app.Shipment', on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat for Shipment {self.shipment.tracking_id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.email} at {self.timestamp}"