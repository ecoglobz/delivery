from django.contrib import admin
from .models import ChatRoom, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp', 'read')
    fields = ('sender', 'content', 'timestamp', 'read')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('get_shipment_id', 'get_customer_name', 'created_at', 'updated_at', 'has_unread')
    search_fields = ('shipment__id', 'shipment__customer__name')
    readonly_fields = ('shipment', 'created_at', 'updated_at')
    inlines = [MessageInline]
    
    def get_shipment_id(self, obj):
        return obj.shipment.id
    get_shipment_id.short_description = 'Shipment ID'
    
    def get_customer_name(self, obj):
        return obj.shipment.customer.name
    get_customer_name.short_description = 'Customer'
    
    def has_unread(self, obj):
        return obj.has_unread_messages(self.request.user)
    has_unread.boolean = True
    has_unread.short_description = 'Unread Messages'
    
    def has_add_permission(self, request):
        return False
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Mark messages as read when admin views the chat
        chat_room = self.get_object(request, object_id)
        if chat_room:
            Message.objects.filter(room=chat_room, read=False).exclude(sender__is_staff=True).update(read=True)
        return super().change_view(request, object_id, form_url, extra_context)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_shipment_id', 'sender', 'short_content', 'timestamp', 'read')
    list_filter = ('read', 'sender__is_staff', 'timestamp')
    search_fields = ('content', 'room__shipment__id', 'sender__username')
    readonly_fields = ('room', 'sender', 'content', 'timestamp')
    
    def get_shipment_id(self, obj):
        return obj.room.shipment.id
    get_shipment_id.short_description = 'Shipment ID'
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
    
    def has_add_permission(self, request):
        return False