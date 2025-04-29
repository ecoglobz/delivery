from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomDetail(generics.RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        shipment_id = self.kwargs['shipment_id']
        return ChatRoom.objects.get(shipment_id=shipment_id)

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shipment_id = self.kwargs['shipment_id']
        room = ChatRoom.objects.get(shipment_id=shipment_id)
        return Message.objects.filter(room=room).order_by('timestamp')

    def perform_create(self, serializer):
        shipment_id = self.kwargs['shipment_id']
        room = ChatRoom.objects.get(shipment_id=shipment_id)
        serializer.save(room=room, sender=self.request.user)