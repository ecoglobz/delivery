from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from .models import Shipment, TrackingEvent, Message

class DashboardAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view)), 
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Calculate time ranges
        today = timezone.now().date()
        thirty_days_ago = today - timezone.timedelta(days=30)

        # Widget Data
        total_shipments = Shipment.objects.count()
        total_customers = Shipment.objects.values('customer_email').distinct().count()
        on_time_delivery = Shipment.objects.filter(status='Delivered').count()
        active_shipments = Shipment.objects.exclude(status__in=['Delivered', 'Exception']).count()

        # Shipment Status Distribution
        status_distribution = (
            Shipment.objects.values('status')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # Shipment Volume Chart Data
        shipment_volume = (
            Shipment.objects.filter(date__gte=thirty_days_ago)
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Recent Shipments
        recent_shipments = Shipment.objects.all().order_by('-date')[:5]

        # Recent Messages
        recent_messages = Message.objects.select_related('room__shipment').order_by('-timestamp')[:5]

        context = {
            **self.admin_site.each_context(request),
            'total_shipments': total_shipments,
            'total_customers': total_customers,
            'on_time_delivery': on_time_delivery,
            'active_shipments': active_shipments,
            'status_distribution': list(status_distribution),
            'shipment_volume': list(shipment_volume),
            'recent_shipments': recent_shipments,
            'recent_messages': recent_messages,
        }
        return render(request, 'admin/dashboard.html', context)

# Replace default admin site
admin.site = DashboardAdmin(name='MyAdmin')