from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'read']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    shipment = serializers.StringRelatedField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'shipment', 'created_at', 'updated_at', 'messages']