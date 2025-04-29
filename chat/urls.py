from django.urls import path
from .views import ChatRoomDetail, MessageList

urlpatterns = [
    path('shipments/<int:shipment_id>/chat/', ChatRoomDetail.as_view(), name='chat-room'),
    path('shipments/<int:shipment_id>/messages/', MessageList.as_view(), name='message-list'),
]