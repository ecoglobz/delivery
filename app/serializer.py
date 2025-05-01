from rest_framework import serializers
from .models import Customer, Shipment, TrackingEvent, Activity

# class CustomerSerializer(serializers.ModelSerializer):
#     shipments = serializers.IntegerField(source='shipments_count', read_only=True)
#     join_date = serializers.DateField(format="%b %d, %Y")
    
#     class Meta:
#         model = Customer
#         fields = '__all__'


# class TrackingEventSerializer(serializers.ModelSerializer):
#     date = serializers.DateTimeField(format="%b %d, %Y - %I:%M %p")
    
#     class Meta:
#         model = TrackingEvent
#         fields = ['id', 'date', 'location', 'description']


# class ShipmentSerializer(serializers.ModelSerializer):
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
#     customer_email = serializers.CharField(source='customer.email', read_only=True)
#     customer_phone = serializers.CharField(source='customer.phone', read_only=True)
#     tracking_events = TrackingEventSerializer(many=True, read_only=True)
#     date = serializers.DateField(format="%b %d, %Y")
#     estimated_delivery = serializers.DateField(format="%b %d, %Y")
#     status_color = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Shipment
#         fields = '__all__'
    
#     def get_status_color(self, obj):
#         status_colors = {
#             'In Transit': 'bg-blue-100 text-blue-800',
#             'Delivered': 'bg-green-100 text-green-800',
#             'Processing': 'bg-yellow-100 text-yellow-800',
#             'Exception': 'bg-red-100 text-red-800',
#         }
#         return status_colors.get(obj.status, 'bg-gray-100 text-gray-800')


# class ActivitySerializer(serializers.ModelSerializer):
#     timestamp = serializers.DateTimeField(format="%b %d, %Y - %I:%M %p")
    
#     class Meta:
#         model = Activity
#         fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone']


class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = ['id', 'date', 'location', 'description', 'created_at']


class ShipmentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Customer.objects.all(), source='customer'
    )
    tracking_events = TrackingEventSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Shipment
        fields = [
            'id', 'customer', 'customer_id', 'origin', 'origin_address',
            'destination', 'destination_address', 'status', 'date',
            'estimated_delivery', 'weight', 'dimensions', 'service',
            'destination_phone_number', 'destination_email', 'destination_name', 'image',
            'created_at', 'updated_at', 'tracking_events'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']     

    def get_image(self, obj):
        return obj.image.url if obj.image else None   
# class ShipmentSerializer(serializers.Serializer):
#     STATUS_CHOICES = (
#         ('Processing', 'Processing'),
#         ('In Transit', 'In Transit'),
#         ('Delivered', 'Delivered'),
#         ('Exception', 'Exception'),
#     )
    
#     SERVICE_CHOICES = (
#         ('Standard International', 'Standard International'),
#         ('Express International', 'Express International'),
#         ('Priority International', 'Priority International'),
#         ('Economy', 'Economy'),
#     )
    
#     id = serializers.CharField(max_length=15)
#     customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
#     origin = serializers.CharField(max_length=100)
#     origin_address = serializers.CharField()
#     destination = serializers.CharField(max_length=100)
#     destination_address = serializers.CharField()
#     status = serializers.ChoiceField(choices=Shipment.STATUS_CHOICES, default='Processing')
#     date = serializers.DateField()
#     estimated_delivery = serializers.DateField(allow_null=True, required=False)
#     weight = serializers.DecimalField(max_digits=10, decimal_places=2)
#     dimensions = serializers.CharField(max_length=50, required=False, allow_blank=True)
#     service = serializers.ChoiceField(choices=Shipment.SERVICE_CHOICES, default='Standard International')
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Shipment.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'action', 'target', 'timestamp']
        read_only_fields = ['timestamp']




class DashboardSerializer(serializers.Serializer):
    stats = serializers.DictField()
    recent_shipments = ShipmentSerializer(many=True)
    recent_activities = ActivitySerializer(many=True)
