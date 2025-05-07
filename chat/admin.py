# # from django.contrib import admin
# # from .models import ChatRoom, Message

# # class MessageInline(admin.TabularInline):
# #     model = Message
# #     extra = 0
# #     readonly_fields = ('sender', 'content', 'timestamp', 'read')
# #     fields = ('sender', 'content', 'timestamp', 'read')
    
# #     def has_add_permission(self, request, obj=None):
# #         return False
    
# #     def has_delete_permission(self, request, obj=None):
# #         return False

# # @admin.register(ChatRoom)
# # class ChatRoomAdmin(admin.ModelAdmin):
# #     list_display = ('get_shipment_id', 'get_customer_name', 'created_at', 'updated_at', 'has_unread')
# #     search_fields = ('shipment__id', 'shipment__customer__name')
# #     readonly_fields = ('shipment', 'created_at', 'updated_at')
# #     inlines = [MessageInline]
    
# #     def get_shipment_id(self, obj):
# #         return obj.shipment.id
# #     get_shipment_id.short_description = 'Shipment ID'
    
# #     def get_customer_name(self, obj):
# #         return obj.shipment.customer.name
# #     get_customer_name.short_description = 'Customer'
    
# #     def has_unread(self, obj):
# #         return obj.has_unread_messages(self.request.user)
# #     has_unread.boolean = True
# #     has_unread.short_description = 'Unread Messages'
    
# #     def has_add_permission(self, request):
# #         return False
    
# #     def change_view(self, request, object_id, form_url='', extra_context=None):
# #         # Mark messages as read when admin views the chat
# #         chat_room = self.get_object(request, object_id)
# #         if chat_room:
# #             Message.objects.filter(room=chat_room, read=False).exclude(sender__is_staff=True).update(read=True)
# #         return super().change_view(request, object_id, form_url, extra_context)

# # @admin.register(Message)
# # class MessageAdmin(admin.ModelAdmin):
# #     list_display = ('get_shipment_id', 'sender', 'short_content', 'timestamp', 'read')
# #     list_filter = ('read', 'sender__is_staff', 'timestamp')
# #     search_fields = ('content', 'room__shipment__id', 'sender__username')
# #     readonly_fields = ('room', 'sender', 'content', 'timestamp')
    
# #     def get_shipment_id(self, obj):
# #         return obj.room.shipment.id
# #     get_shipment_id.short_description = 'Shipment ID'
    
# #     def short_content(self, obj):
# #         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
# #     short_content.short_description = 'Content'
    
# #     def has_add_permission(self, request):
# #         return False

# from django.contrib import admin
# from .models import Message
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('short_content', 'is_admin', 'timestamp')
#     list_filter = ('is_admin', 'timestamp')
#     actions = ['reply_to_message']

#     def short_content(self, obj):
#         return obj.content[:50]
#     short_content.short_description = 'Content'

#     def save_model(self, request, obj, form, change):
#         if not change:  # Only for new messages
#             if request.user.is_staff:
#                 obj.is_admin = True
#                 obj.user = request.user
#         super().save_model(request, obj, form, change)
        
#         # Send message via WebSocket
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"chat_{obj.room}",
#             {
#                 "type": "chat.message",
#                 "message": obj.content,
#                 "is_admin": obj.is_admin
#             }
#         )

#     def reply_to_message(self, request, queryset):
#         selected = queryset.first()
#         return HttpResponseRedirect(
#             reverse('admin:chat_message_add') + 
#             f'?initial={selected.id}&room={selected.room}'
#         )
#     reply_to_message.short_description = "Reply to selected message"

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         initial = request.GET.get('initial')
#         room = request.GET.get('room', 'public')
        
#         if initial:
#             original = Message.objects.get(id=initial)
#             form.base_fields['content'].initial = f"Re: {original.content[:50]}..."
#             form.base_fields['room'].initial = original.room
#         else:
#             form.base_fields['room'].initial = room
#         return form


# chat/admin.py
# from django.contrib import admin
# from .models import ChatSession, Message

# class MessageInline(admin.StackedInline):
#     model = Message
#     fields = ("sender", "content", "timestamp")
#     readonly_fields = ("timestamp",)
#     extra = 0
#     ordering = ("timestamp",)  # show messages in chronological order

# class ChatSessionAdmin(admin.ModelAdmin):
#     list_display = ("id", "email", "created")
#     readonly_fields = ("email", "created")
#     inlines = [MessageInline]

# admin.site.register(ChatSession, ChatSessionAdmin)


# from django.contrib import admin
# from django.utils.safestring import mark_safe
# from django.urls import path
# from django.template.response import TemplateResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from .models import ChatSession, Message

# class ChatSessionAdmin(admin.ModelAdmin):
#     change_form_template = "admin/chat/chatsession/change_form.html"
#     list_display = ("email", "created")
#     readonly_fields = ("email", "created")

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("<int:session_id>/send/", self.admin_site.admin_view(self.send_message_view), name="chat_send_message"),
#             path("<int:session_id>/messages/", self.admin_site.admin_view(self.get_messages_view), name="chat_get_messages"),
#         ]
#         return custom_urls + urls

#     @method_decorator(csrf_exempt)
#     def send_message_view(self, request, session_id):
#         if request.method == "POST":
#             content = request.POST.get("content")
#             if content:
#                 Message.objects.create(chat_id=session_id, sender="admin", content=content)
#                 return JsonResponse({"status": "success"})
#         return JsonResponse({"status": "failed"})

#     def get_messages_view(self, request, session_id):
#         messages = Message.objects.filter(chat_id=session_id).order_by("timestamp")
#         data = [
#             {
#                 "id": m.id,
#                 "sender": m.sender,
#                 "content": m.content,
#                 "timestamp": m.timestamp.strftime("%H:%M:%S")
#             }
#             for m in messages
#         ]
#         return JsonResponse({"messages": data})

# admin.site.register(ChatSession, ChatSessionAdmin)
# admin.site.register(Message)

# # chat/admin.py
# from django.contrib import admin
# from django.utils.safestring import mark_safe
# from django.urls import path
# from django.template.response import TemplateResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from .models import ChatSession, Message

# class ChatSessionAdmin(admin.ModelAdmin):
#     change_form_template = "admin/chat/chatsession/change_form.html"
#     list_display = ("email", "created")
#     readonly_fields = ("email", "created")

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("<int:session_id>/send/", self.admin_site.admin_view(self.send_message_view), name="chat_send_message"),
#             path("<int:session_id>/messages/", self.admin_site.admin_view(self.get_messages_view), name="chat_get_messages"),
#         ]
#         return custom_urls + urls

#     @method_decorator(csrf_exempt)
#     def send_message_view(self, request, session_id):
#         if request.method == "POST":
#             content = request.POST.get("content")
#             if content:
#                 print("Saving message:", content)
#                 Message.objects.create(chat_id=session_id, sender="admin", content=content)
#                 return JsonResponse({"status": "success"})
#         return JsonResponse({"status": "failed"})

#     def get_messages_view(self, request, session_id):
#         messages = Message.objects.filter(chat_id=session_id).order_by("timestamp")
#         data = [
#             {
#                 "id": m.id,
#                 "sender": m.sender,
#                 "content": m.content,
#                 "timestamp": m.timestamp.strftime("%H:%M:%S")
#             }
#             for m in messages
#         ]
#         return JsonResponse({"messages": data})

# admin.site.register(ChatSession, ChatSessionAdmin)
# admin.site.register(Message)

# # chat/templates/admin/chat/chatsession/change_form.html


from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import ChatSession, Message

class ChatSessionAdmin(admin.ModelAdmin):
    change_form_template = "admin/chat/chatsession/change_form.html"
    list_display = ("email", "created")
    readonly_fields = ("email", "created")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:session_id>/send/", self.admin_site.admin_view(self.send_message_view), name="chat_send_message"),
            path("<int:session_id>/messages/", self.admin_site.admin_view(self.get_messages_view), name="chat_get_messages"),
        ]
        return custom_urls + urls

    @method_decorator(csrf_exempt)
    def send_message_view(self, request, session_id):
        if request.method == "POST":
            content = request.POST.get("content")
            if content:
                print("Saving message:", content)
                Message.objects.create(chat_id=session_id, sender="admin", content=content)
                return JsonResponse({"status": "success"})
        return JsonResponse({"status": "failed"})

    def get_messages_view(self, request, session_id):
        messages = Message.objects.filter(chat_id=session_id).order_by("timestamp")
        session = ChatSession.objects.get(id=session_id)
        data = {
            "email": session.email,
            "messages": [
                {
                    "id": m.id,
                    "sender": m.sender,
                    "content": m.content,
                    "timestamp": m.timestamp.strftime("%H:%M:%S")
                }
                for m in messages
            ]
        }
        return JsonResponse(data)

admin.site.register(ChatSession, ChatSessionAdmin)
admin.site.register(Message)