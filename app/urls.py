"""
URL Configuration for shipping_management project.
"""

from django.urls import path, include
from rest_framework import routers
from .views import CustomerViewSet, ShipmentTrackingView

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
# router.register(r'shipments', ShipmentViewSet, basename='shipment')

urlpatterns = [
    path('', include(router.urls)),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("shipments/<str:tracking_id>/", ShipmentTrackingView.as_view(), name="shipment-tracking")
    # path('shipments/', ShipmentListCreateAPIView.as_view(), name='shipment-list-create'),
]
