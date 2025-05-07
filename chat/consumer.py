# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser
# from .models import ChatRoom, Message
# from app.models import Shipment

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.shipment_id = self.scope['url_route']['kwargs']['shipment_id']
#         self.room_group_name = f'chat_{self.shipment_id}'

#         # Check if shipment exists and create chat room if needed
#         shipment_exists = await self.get_or_create_chat_room()
#         if not shipment_exists:
#             await self.close()
#             return

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender_id = text_data_json['sender_id']

#         # Save message to database
#         message_obj = await self.save_message(sender_id, message)
#         if not message_obj:
#             return

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender_id': sender_id,
#                 'timestamp': str(message_obj.timestamp),
#                 'message_id': message_obj.id,
#             }
#         )

#     async def chat_message(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender_id': event['sender_id'],
#             'timestamp': event['timestamp'],
#             'message_id': event['message_id'],
#         }))

#     @database_sync_to_async
#     def get_or_create_chat_room(self):
#         try:
#             shipment = Shipment.objects.get(id=self.shipment_id)
#             ChatRoom.objects.get_or_create(shipment=shipment)
#             return True
#         except Shipment.DoesNotExist:
#             return False

#     @database_sync_to_async
#     def save_message(self, sender_id, content):
#         try:
#             shipment = Shipment.objects.get(id=self.shipment_id)
#             room, created = ChatRoom.objects.get_or_create(shipment=shipment)
            
#             # Get the user from sender_id
#             from django.contrib.auth import get_user_model
#             User = get_user_model()
            
#             try:
#                 sender = User.objects.get(id=sender_id)
#             except User.DoesNotExist:
#                 # If customer isn't authenticated, create or get a special admin user for system messages
#                 sender, created = User.objects.get_or_create(
#                     username='customer',
#                     defaults={'email': 'customer@example.com', 'is_staff': False}
#                 )
            
#             message = Message.objects.create(
#                 room=room,
#                 sender=sender,
#                 content=content
#             )
            
#             # Notify admins about new customer messages (you can implement this later)
#             if not sender.is_staff:
#                 # TODO: Send notification to admins
#                 pass
                
#             return message
#         except Exception as e:
#             print(f"Error saving message: {e}")
#             return None

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'public')
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json.get('room', 'public')

        # Save user message (unauthenticated)
        Message.objects.create(
            content=message,
            is_admin=False,
            room=room
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'is_admin': False
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'is_admin': event['is_admin']
        }))