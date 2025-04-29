# from django.contrib import admin
# from .models import Customer, Shipment, TrackingEvent, Activity



# class TrackingEventInline(admin.TabularInline):
#     model = TrackingEvent
#     extra = 1


# @admin.register(Shipment)
# class ShipmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'origin', 'destination', 'status', 'date', 'service')
#     list_filter = ('status', 'service', 'date')
#     search_fields = ('id', 'customer__name', 'origin', 'destination')
#     date_hierarchy = 'date'
#     inlines = [TrackingEventInline]


# @admin.register(TrackingEvent)
# class TrackingEventAdmin(admin.ModelAdmin):
#     list_display = ('shipment', 'date', 'location', 'description')
#     list_filter = ('date',)
#     search_fields = ('shipment__id', 'location', 'description')
#     date_hierarchy = 'date'


# @admin.register(Activity)
# class ActivityAdmin(admin.ModelAdmin):
#     list_display = ('user', 'action', 'target', 'timestamp')
#     list_filter = ('timestamp', 'user')
#     search_fields = ('user', 'action', 'target')
#     date_hierarchy = 'timestamp'

from django.contrib import admin
from django.utils import timezone
from .models import Shipment, TrackingEvent, Activity, Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'email', 'type', 'status', 'join_date')
    list_filter = ('type', 'status', 'country')
    search_fields = ('id', 'name', 'company', 'email')
    date_hierarchy = 'join_date'


class TrackingEventInline(admin.TabularInline):
    model = TrackingEvent
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('date', 'location', 'description', 'created_at')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'origin', 'destination', 'status', 'date', 'estimated_delivery')
    list_filter = ('status', 'service', 'date')
    search_fields = ('id', 'customer__name', 'origin', 'destination')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [TrackingEventInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Record activity
        Activity.objects.create(
            user=request.user.username,
            action="updated" if change else "created",
            target=f"Shipment {obj.id}"
        )

@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'date', 'location', 'description')
    list_filter = ('date', 'location')
    search_fields = ('shipment__id', 'location', 'description')
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Record activity
        Activity.objects.create(
            user=request.user.username,
            action="updated" if change else "created",
            target=f"Tracking event for {obj.shipment.id}"
        )
        
        # Update shipment status based on tracking event description
        shipment = obj.shipment
        description = obj.description.lower()
        
        if "delivered" in description:
            shipment.status = "Delivered"
        elif "exception" in description or "failed" in description:
            shipment.status = "Exception"
        elif "transit" in description or "departed" in description:
            shipment.status = "In Transit"
        
        shipment.save(update_fields=['status'])

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'target', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user', 'action', 'target')
    readonly_fields = ('user', 'action', 'target', 'timestamp')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False