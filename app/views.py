from django.shortcuts import render

# Create your views here.
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import viewsets, views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from datetime import timedelta
from .models import Customer, Shipment, TrackingEvent, Activity
from .serializer import (
    CustomerSerializer, ShipmentSerializer, 
    TrackingEventSerializer, ActivitySerializer,
    DashboardSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) |
                Q(name__icontains=search) |
                Q(company__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by type
        customer_type = self.request.query_params.get('type', None)
        if customer_type and customer_type != 'all':
            queryset = queryset.filter(type__iexact=customer_type)
        
        # Sorting
        sort_by = self.request.query_params.get('sort_by', 'name')
        sort_order = self.request.query_params.get('sort_order', 'asc')
        
        if sort_by == 'shipments':
            # Annotate with shipment count for sorting
            queryset = queryset.annotate(shipment_count=Count('shipment'))
            sort_field = 'shipment_count'
        elif sort_by == 'joinDate':
            sort_field = 'join_date'
        else:
            sort_field = sort_by
        
        if sort_order == 'desc':
            sort_field = f'-{sort_field}'
        
        return queryset.order_by(sort_field)
    
    def perform_create(self, serializer):
        customer = serializer.save()
        # Log activity
        Activity.objects.create(
            user="Admin",
            action="created a new customer",
            target=customer.name
        )
    
    def perform_update(self, serializer):
        customer = serializer.save()
        # Log activity
        Activity.objects.create(
            user="Admin",
            action="updated customer",
            target=customer.name
        )
    
    def perform_destroy(self, instance):
        # Log activity
        Activity.objects.create(
            user="Admin",
            action="deleted customer",
            target=instance.name
        )
        instance.delete()


# class ShipmentViewSet(viewsets.ViewSet):
#     """
#     API endpoint for managing shipments
#     """
    
#     def list(self, request):
#         # Get query parameters
#         customer_id = request.query_params.get('customer_id', None)
        
#         # Filter by customer if provided
#         if customer_id:
#             shipments = Shipment.get_customer_shipments(customer_id)
#         else:
#             shipments = Shipment.objects.all()
        
#         serializer = ShipmentSerializer(shipments, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = ShipmentSerializer(data=request.data)
#         if serializer.is_valid():
#             # Extract data from validated serializer
#             data = serializer.validated_data
            
#             # Create shipment using classmethod
#             shipment = Shipment.create_shipment(
#                 customer=data['customer'],
#                 origin=data['origin'],
#                 origin_address=data['origin_address'],
#                 destination=data['destination'],
#                 destination_address=data['destination_address'],
#                 weight=data['weight'],
#                 dimensions=data.get('dimensions', ''),
#                 service=data.get('service', 'Standard International'),
#                 status=data.get('status', 'Processing'),
#                 date=data.get('date'),
#                 estimated_delivery=data.get('estimated_delivery')
#             )
            
#             result_serializer = ShipmentSerializer(shipment)
#             print(result_serializer.data, "shipment created")
#             return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def retrieve(self, request, pk=None):
#         shipment = Shipment.get_shipment(pk)
#         # print(shipment, "shipment retrieved", dir(shipment))
#         if shipment:
#             serializer = ShipmentSerializer(shipment)
#             return Response(serializer.data)
#         return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     def update(self, request, pk=None):
#         serializer = ShipmentSerializer(data=request.data, partial=True)
#         if serializer.is_valid():
#             # Extract data from validated serializer
#             data = serializer.validated_data
            
#             # Remove customer from update fields if present
#             if 'customer' in data:
#                 data.pop('customer')
            
#             # Update shipment using classmethod
#             updated_shipment = Shipment.update_shipment(pk, **data)
            
#             if updated_shipment:
#                 result_serializer = ShipmentSerializer(updated_shipment)
#                 return Response(result_serializer.data)
            
#             return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def partial_update(self, request, pk=None):
#         return self.update(request, pk)
    
#     def destroy(self, request, pk=None):
#         success = Shipment.delete_shipment(pk)
#         if success:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     @action(detail=True, methods=['post'])
#     def update_status(self, request, pk=None):
#         """
#         Update a shipment's status and create a tracking event
#         """
#         new_status = request.data.get('status')
#         location = request.data.get('location')
        
#         if not new_status:
#             return Response(
#                 {"detail": "Status field is required"}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         updated_shipment = Shipment.update_status(pk, new_status, location)
        
#         if updated_shipment:
#             serializer = ShipmentSerializer(updated_shipment)
#             return Response(serializer.data)
        
#         return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)


# class ShipmentListCreateAPIView(APIView):
#     def get(self, request):
#         shipments = Shipment.objects.all()
#         serializer = ShipmentSerializer(shipments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         print(request.data, "shipment data")
#         serializer = ShipmentSerializer(data=request.data)
#         if serializer.is_valid():
#             print(serializer.validated_data, "validated data")
#             shipment = serializer.save()
#             return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ShipmentTrackingView(APIView):
    """
    View for tracking a shipment by its tracking ID
    """
    def get(self, request, tracking_id):
        shipment = Shipment.get_shipment_by_tracking_id(tracking_id)
        if shipment:
            serializer = ShipmentSerializer(shipment)
            return Response(serializer.data)
        return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
    

class DashboardView(views.APIView):
    def get(self, request):
        # Get stats
        active_shipments_count = Shipment.objects.filter(
            status__in=['Processing', 'In Transit']
        ).count()
        
        customers_count = Customer.objects.count()
        
        # For demo purposes, let's say we have a fixed number of drivers
        available_drivers = 78
        
        delayed_shipments_count = Shipment.objects.filter(
            status='Exception'
        ).count()
        
        # Calculate month-over-month changes (dummy data for demo)
        stats = {
            'active_shipments': {
                'value': active_shipments_count,
                'change': '+12.5%',
                'trend': 'up',
            },
            'customers': {
                'value': customers_count,
                'change': '+5.2%',
                'trend': 'up',
            },
            'available_drivers': {
                'value': available_drivers,
                'change': '-3.1%',
                'trend': 'down',
            },
            'delayed_shipments': {
                'value': delayed_shipments_count,
                'change': '+2.3%',
                'trend': 'up',
            },
        }
        
        # Get recent shipments
        recent_shipments = Shipment.objects.all().order_by('-date')[:5]
        
        # Get recent activities
        recent_activities = Activity.objects.all()[:5]
        
        # Prepare data for serialization
        dashboard_data = {
            'stats': stats,
            'recent_shipments': recent_shipments,
            'recent_activities': recent_activities,
        }
        
        serializer = DashboardSerializer(dashboard_data)
        return Response(serializer.data)
