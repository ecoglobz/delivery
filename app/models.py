from django.db import models
from django.utils import timezone

class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('Business', 'Business'),
        ('Individual', 'Individual'),
    )
    
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    
    id = models.CharField(primary_key=True, max_length=10)  # Custom ID like CUST001
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='Business')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True)
    join_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def shipments_count(self):
        return self.shipment_set.count()
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a custom ID if not provided
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer:
                last_id = int(last_customer.id[4:])
                self.id = f"CUST{last_id + 1:03d}"
            else:
                self.id = "CUST001"
        super().save(*args, **kwargs)


# class Shipment(models.Model):
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
    
#     id = models.CharField(primary_key=True, max_length=15)  # Custom ID like CRU7327510138
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     origin = models.CharField(max_length=100)
#     origin_address = models.TextField()
#     destination = models.CharField(max_length=100)
#     destination_address = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
#     date = models.DateField(default=timezone.now)
#     estimated_delivery = models.DateField(null=True, blank=True)
#     weight = models.DecimalField(max_digits=10, decimal_places=2)
#     dimensions = models.CharField(max_length=50, blank=True)
#     service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='Standard International')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.id} - {self.customer.name}"
    
#     def save(self, *args, **kwargs):
#         is_new = not self.pk  # Check if this is a new shipment
#         print("is new ", is_new)
        
#         if not self.id:
#             # Generate a custom ID if not provided
#             import random
#             self.id = f"CRU{random.randint(1000000000, 9999999999)}"
        
#         super().save(*args, **kwargs)
        
#         # Create initial tracking event for new shipments
#         if is_new:
#             from .models import TrackingEvent  # Import here to avoid circular imports
            
#             TrackingEvent.objects.create(
#                 shipment=self,
#                 date=timezone.now(),
#                 location=self.origin,
#                 description=f"Shipment created at {self.origin}"
#             )


# class TrackingEvent(models.Model):
#     shipment = models.ForeignKey(Shipment, related_name='tracking_events', on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     location = models.CharField(max_length=100)
#     description = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['-date']
    
#     def __str__(self):
#         return f"{self.shipment.id} - {self.date} - {self.description}"


# class Activity(models.Model):
#     user = models.CharField(max_length=100)
#     action = models.CharField(max_length=255)
#     target = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['-timestamp']
#         verbose_name_plural = 'Activities'
    
#     def __str__(self):
#         return f"{self.user} {self.action} {self.target}"

# Shipment Model CRUD Classmethods
class Shipment(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Exception', 'Exception'),
    )
    
    SERVICE_CHOICES = (
        ('Standard International', 'Standard International'),
        ('Express International', 'Express International'),
        ('Priority International', 'Priority International'),
        ('Economy', 'Economy'),
    )
    
    id = models.CharField(primary_key=True, max_length=15)  # Custom ID like CRU7327510138
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    origin_address = models.TextField()
    destination = models.CharField(max_length=100)
    destination_address = models.TextField()
    destination_phone_number = models.CharField(max_length=20, blank=True, null=True)
    destination_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    date = models.DateField(default=timezone.now)
    estimated_delivery = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=50, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='Standard International')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} - {self.customer.name}"
    
    @classmethod
    def get_fields(cls):
        """
        Get all fields of the Shipment model.
        
        Returns:
            List of field names
        """
        return [
            "customer__name",
            "customer__company",
            "customer__email",
            "customer__phone",
            "customer__address",
            "origin",
            "destination",
            "status",
            "date",
            "estimated_delivery",
            "weight",
            "dimensions",
            "service",
            "origin_address",
        ]
    
    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if this is a new shipment
        print("is new ", is_new)
        
        if not self.id:
            # Generate a custom ID if not provided
            import random
            self.id = f"CRU{random.randint(1000000000, 9999999999)}"
        
        super().save(*args, **kwargs)
        
        # Create initial tracking event for new shipments
        if is_new:
            from .models import TrackingEvent  # Import here to avoid circular imports
            
            TrackingEvent.objects.create(
                shipment=self,
                date=timezone.now(),
                location=self.origin,
                description=f"Shipment created at {self.origin}"
            )
    
    @classmethod
    def create_shipment(cls, customer, origin, origin_address, destination, destination_address, 
                        weight, dimensions='', service='Standard International', 
                        status='Processing', date=None, estimated_delivery=None, shipment_id=None):
        """
        Create a new shipment with the provided details.
        
        Args:
            customer: Customer object
            origin: Origin location name
            origin_address: Full origin address
            destination: Destination location name
            destination_address: Full destination address
            weight: Shipment weight
            dimensions: Optional package dimensions
            service: Shipping service type
            status: Initial shipment status
            date: Shipment date
            estimated_delivery: Estimated delivery date
            shipment_id: Optional custom shipment ID
            
        Returns:
            Newly created Shipment object
        """
        if date is None:
            date = timezone.now().date()
        
        print("shipment_id ")   
            
        shipment = cls.objects.create(
            id=shipment_id,  # Will be auto-generated in save() if None
            customer=customer,
            origin=origin,
            origin_address=origin_address,
            destination=destination,
            destination_address=destination_address,
            status=status,
            date=date,
            estimated_delivery=estimated_delivery,
            weight=weight,
            dimensions=dimensions,
            service=service
        )

        print("shipment created ", shipment)

        
        
        # Log activity
        Activity.create_activity(
            user=customer.name,
            action="created",
            target=f"shipment {shipment.id}"
        )
        
        return shipment
    
    @classmethod
    def get_shipment(cls, shipment_id):
        """
        Retrieve a shipment by its ID.
        
        Args:
            shipment_id: The ID of the shipment to retrieve
            
        Returns:
            Shipment object or None if not found
        """
        try:
            return cls.objects.filter(id=shipment_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_customer_shipments(cls, customer_id):
        """
        Get all shipments for a specific customer.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            QuerySet of Shipment objects
        """
        return cls.objects.filter(customer_id=customer_id)
    
    @classmethod
    def update_shipment(cls, shipment_id, **kwargs):
        """
        Update a shipment's details.
        
        Args:
            shipment_id: ID of the shipment to update
            **kwargs: Fields to update and their new values
            
        Returns:
            Updated Shipment object or None if not found
        """
        try:
            shipment = cls.objects.get(id=shipment_id)
            
            # Update allowed fields
            allowed_fields = [
                'origin', 'origin_address', 'destination', 'destination_address',
                'status', 'date', 'estimated_delivery', 'weight', 'dimensions', 'service'
            ]
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(shipment, field, value)
            
            shipment.save()
            
            # Log activity
            Activity.create_activity(
                user="system",  # This should be replaced with actual user when available
                action="updated",
                target=f"shipment {shipment.id}"
            )
            
            return shipment
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def delete_shipment(cls, shipment_id):
        """
        Delete a shipment by its ID.
        
        Args:
            shipment_id: ID of the shipment to delete
            
        Returns:
            True if successful, False if shipment not found
        """
        try:
            shipment = cls.objects.get(id=shipment_id)
            
            # Store info for activity log before deletion
            customer_name = shipment.customer.name
            shipment_id_str = shipment.id
            
            shipment.delete()
            
            # Log activity
            Activity.create_activity(
                user="system",  # This should be replaced with actual user when available
                action="deleted",
                target=f"shipment {shipment_id_str}"
            )
            
            return True
        except cls.DoesNotExist:
            return False
    
    @classmethod
    def update_status(cls, shipment_id, new_status, location=None):
        """
        Update a shipment's status and create a tracking event.
        
        Args:
            shipment_id: ID of the shipment to update
            new_status: New status value
            location: Current location for the tracking event
            
        Returns:
            Updated Shipment object or None if not found
        """
        try:
            shipment = cls.objects.get(id=shipment_id)
            old_status = shipment.status
            shipment.status = new_status
            shipment.save()
            
            # Create tracking event for status change
            from .models import TrackingEvent
            
            if location is None:
                location = shipment.origin if new_status == 'Processing' else shipment.destination
            
            TrackingEvent.create_event(
                shipment=shipment,
                location=location,
                description=f"Status changed from {old_status} to {new_status}"
            )
            
            # Log activity
            Activity.create_activity(
                user="system",  # This should be replaced with actual user when available
                action="updated status of",
                target=f"shipment {shipment.id} to {new_status}"
            )
            
            return shipment
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_shipment_by_tracking_id(cls, tracking_id):
        """
        Retrieve a shipment by tracking ID with all related data.
        
        Args:
            tracking_id: The tracking ID/shipment ID
            
        Returns:
            Shipment object with customer and tracking events or None if not found
        """
        try:
            return cls.objects.select_related('customer').prefetch_related('tracking_events').get(id=tracking_id)
        except cls.DoesNotExist:
            return None



# TrackingEvent Model CRUD Classmethods
class TrackingEvent(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='tracking_events', on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.shipment.id} - {self.date} - {self.description}"
    
    @classmethod
    def create_event(cls, shipment, location, description, date=None):
        """
        Create a new tracking event for a shipment.
        
        Args:
            shipment: Shipment object
            location: Current location
            description: Event description
            date: Event date and time (defaults to now)
            
        Returns:
            Newly created TrackingEvent object
        """
        if date is None:
            date = timezone.now()
            
        event = cls(
            shipment=shipment,
            date=date,
            location=location,
            description=description
        )
        event.save()
        
        # Log activity
        Activity.create_activity(
            user="system",  # This should be replaced with actual user when available
            action="added tracking event to",
            target=f"shipment {shipment.id}"
        )
        
        return event
    
    @classmethod
    def get_shipment_events(cls, shipment_id):
        """
        Get all tracking events for a specific shipment.
        
        Args:
            shipment_id: ID of the shipment
            
        Returns:
            QuerySet of TrackingEvent objects
        """
        return cls.objects.filter(shipment_id=shipment_id)
    
    @classmethod
    def get_event(cls, event_id):
        """
        Retrieve a tracking event by its ID.
        
        Args:
            event_id: The ID of the event to retrieve
            
        Returns:
            TrackingEvent object or None if not found
        """
        try:
            return cls.objects.get(id=event_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_event(cls, event_id, **kwargs):
        """
        Update a tracking event's details.
        
        Args:
            event_id: ID of the event to update
            **kwargs: Fields to update and their new values
            
        Returns:
            Updated TrackingEvent object or None if not found
        """
        try:
            event = cls.objects.get(id=event_id)
            
            # Update allowed fields
            allowed_fields = ['date', 'location', 'description']
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(event, field, value)
            
            event.save()
            
            # Log activity
            Activity.create_activity(
                user="system",  # This should be replaced with actual user when available
                action="updated tracking event for",
                target=f"shipment {event.shipment.id}"
            )
            
            return event
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def delete_event(cls, event_id):
        """
        Delete a tracking event by its ID.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            True if successful, False if event not found
        """
        try:
            event = cls.objects.get(id=event_id)
            
            # Store info for activity log before deletion
            shipment_id = event.shipment.id
            
            event.delete()
            
            # Log activity
            Activity.create_activity(
                user="system",  # This should be replaced with actual user when available
                action="deleted tracking event from",
                target=f"shipment {shipment_id}"
            )
            
            return True
        except cls.DoesNotExist:
            return False
    
    


# Activity Model CRUD Classmethods
class Activity(models.Model):
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user} {self.action} {self.target}"
    
    @classmethod
    def create_activity(cls, user, action, target):
        """
        Create a new activity log entry.
        
        Args:
            user: User who performed the action
            action: Description of the action performed
            target: Target of the action
            
        Returns:
            Newly created Activity object
        """
        activity = cls(
            user=user,
            action=action,
            target=target
        )
        activity.save()
        return activity
    
    @classmethod
    def get_recent_activities(cls, limit=50):
        """
        Get the most recent activities.
        
        Args:
            limit: Maximum number of activities to return
            
        Returns:
            QuerySet of Activity objects
        """
        return cls.objects.all()[:limit]
    
    @classmethod
    def get_user_activities(cls, user, limit=50):
        """
        Get activities for a specific user.
        
        Args:
            user: User to filter activities for
            limit: Maximum number of activities to return
            
        Returns:
            QuerySet of Activity objects
        """
        return cls.objects.filter(user=user)[:limit]
    
    @classmethod
    def get_activity(cls, activity_id):
        """
        Retrieve an activity by its ID.
        
        Args:
            activity_id: The ID of the activity to retrieve
            
        Returns:
            Activity object or None if not found
        """
        try:
            return cls.objects.get(id=activity_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def delete_activity(cls, activity_id):
        """
        Delete an activity log entry by its ID.
        
        Args:
            activity_id: ID of the activity to delete
            
        Returns:
            True if successful, False if activity not found
        """
        try:
            activity = cls.objects.get(id=activity_id)
            activity.delete()
            return True
        except cls.DoesNotExist:
            return False
    
    @classmethod
    def clear_old_activities(cls, days=30):
        """
        Delete activities older than the specified number of days.
        
        Args:
            days: Number of days to keep activities for
            
        Returns:
            Number of activities deleted
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        old_activities = cls.objects.filter(timestamp__lt=cutoff_date)
        count = old_activities.count()
        old_activities.delete()
        return count