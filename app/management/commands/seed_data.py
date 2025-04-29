from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Customer, Shipment, TrackingEvent, Activity
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Activity.objects.all().delete()
        TrackingEvent.objects.all().delete()
        Shipment.objects.all().delete()
        Customer.objects.all().delete()
        
        # Create customers
        self.stdout.write('Creating customers...')
        customers = [
            {
                'name': 'Vicki Negron',
                'company': 'Negron Shipping LLC',
                'email': 'vicki.negron@example.com',
                'phone': '+1 (802) 289-1119',
                'address': '123 Main St',
                'city': 'Burlington',
                'state': 'VT',
                'postal_code': '05401',
                'country': 'United States',
                'type': 'Business',
                'status': 'Active',
                'join_date': timezone.now() - timedelta(days=100),
            },
            {
                'name': 'John Smith',
                'company': 'Global Trade Co.',
                'email': 'john.smith@example.com',
                'phone': '+1 (555) 123-4567',
                'address': '456 Market St',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10001',
                'country': 'United States',
                'type': 'Business',
                'status': 'Active',
                'join_date': timezone.now() - timedelta(days=400),
            },
            {
                'name': 'Sarah Johnson',
                'company': 'Johnson Imports',
                'email': 'sarah.johnson@example.com',
                'phone': '+1 (555) 987-6543',
                'address': '789 Queen St',
                'city': 'Toronto',
                'state': 'ON',
                'postal_code': 'M5V 2A8',
                'country': 'Canada',
                'type': 'Business',
                'status': 'Active',
                'join_date': timezone.now() - timedelta(days=170),
            },
            {
                'name': 'Michael Chen',
                'company': '',
                'email': 'michael.chen@example.com',
                'phone': '+49 30 12345678',
                'address': '10 Berlin Strasse',
                'city': 'Berlin',
                'state': '',
                'postal_code': '10115',
                'country': 'Germany',
                'type': 'Individual',
                'status': 'Inactive',
                'join_date': timezone.now() - timedelta(days=320),
            },
            {
                'name': 'Elena Rodriguez',
                'company': 'Rodriguez Exports S.L.',
                'email': 'elena.rodriguez@example.com',
                'phone': '+34 91 123 4567',
                'address': 'Calle Gran Via 1',
                'city': 'Madrid',
                'state': '',
                'postal_code': '28013',
                'country': 'Spain',
                'type': 'Business',
                'status': 'Active',
                'join_date': timezone.now() - timedelta(days=430),
            },
        ]
        
        created_customers = []
        for customer_data in customers:
            customer = Customer.objects.create(**customer_data)
            created_customers.append(customer)
            self.stdout.write(f'Created customer: {customer.name}')
        
        # Create shipments
        self.stdout.write('Creating shipments...')
        shipments_data = [
            {
                'customer': created_customers[0],
                'origin': 'Abu Dhabi, UAE',
                'origin_address': '21 Marina Street, Downtown Abu Dhabi, UAE',
                'destination': 'Chester, VT, USA',
                'destination_address': '145 Main Street, Chester, VT 05143, USA',
                'status': 'In Transit',
                'date': timezone.now() - timedelta(days=10),
                'estimated_delivery': timezone.now() + timedelta(days=4),
                'weight': 31.2,
                'dimensions': '45 × 35 × 25',
                'service': 'Express International',
            },
            {
                'customer': created_customers[1],
                'origin': 'London, UK',
                'origin_address': '10 Downing Street, London, UK',
                'destination': 'New York, NY, USA',
                'destination_address': '350 Fifth Avenue, New York, NY 10118, USA',
                'status': 'Delivered',
                'date': timezone.now() - timedelta(days=11),
                'estimated_delivery': timezone.now() - timedelta(days=5),
                'weight': 18.5,
                'dimensions': '30 × 25 × 20',
                'service': 'Standard International',
            },
            {
                'customer': created_customers[2],
                'origin': 'Tokyo, Japan',
                'origin_address': '1-1 Marunouchi, Chiyoda-ku, Tokyo, Japan',
                'destination': 'Sydney, Australia',
                'destination_address': '1 Harbour Street, Sydney NSW 2000, Australia',
                'status': 'Processing',
                'date': timezone.now() - timedelta(days=11),
                'estimated_delivery': timezone.now() + timedelta(days=7),
                'weight': 42.7,
                'dimensions': '50 × 40 × 30',
                'service': 'Express International',
            },
            {
                'customer': created_customers[3],
                'origin': 'Berlin, Germany',
                'origin_address': 'Unter den Linden 77, 10117 Berlin, Germany',
                'destination': 'Paris, France',
                'destination_address': '16 Rue de Rivoli, 75001 Paris, France',
                'status': 'Exception',
                'date': timezone.now() - timedelta(days=12),
                'estimated_delivery': timezone.now() - timedelta(days=6),
                'weight': 15.3,
                'dimensions': '25 × 20 × 15',
                'service': 'Standard International',
            },
            {
                'customer': created_customers[4],
                'origin': 'Madrid, Spain',
                'origin_address': 'Calle de Alcalá 1, 28014 Madrid, Spain',
                'destination': 'Rome, Italy',
                'destination_address': 'Via del Corso 1, 00186 Roma RM, Italy',
                'status': 'Delivered',
                'date': timezone.now() - timedelta(days=12),
                'estimated_delivery': timezone.now() - timedelta(days=6),
                'weight': 8.9,
                'dimensions': '20 × 15 × 10',
                'service': 'Express International',
            },
        ]
        
        created_shipments = []
        for shipment_data in shipments_data:
            shipment = Shipment.objects.create(**shipment_data)
            created_shipments.append(shipment)
            self.stdout.write(f'Created shipment: {shipment.id}')
            
            # Create tracking events for each shipment
            if shipment.status == 'In Transit':
                events = [
                    {
                        'date': timezone.now() - timedelta(days=10, hours=15, minutes=30),
                        'location': 'Online',
                        'description': 'Shipping label created',
                    },
                    {
                        'date': timezone.now() - timedelta(days=9, hours=9, minutes=45),
                        'location': f'{shipment.origin}',
                        'description': 'Shipment picked up',
                    },
                    {
                        'date': timezone.now() - timedelta(days=8, hours=21, minutes=15),
                        'location': f'{shipment.origin} Sorting Center',
                        'description': 'Shipment processed at sorting facility',
                    },
                    {
                        'date': timezone.now() - timedelta(days=7, hours=8, minutes=30),
                        'location': f'{shipment.origin} International Airport',
                        'description': 'Shipment departed from origin airport',
                    },
                ]
            elif shipment.status == 'Delivered':
                events = [
                    {
                        'date': timezone.now() - timedelta(days=12, hours=10, minutes=20),
                        'location': 'Online',
                        'description': 'Shipping label created',
                    },
                    {
                        'date': timezone.now() - timedelta(days=11, hours=14, minutes=45),
                        'location': f'{shipment.origin}',
                        'description': 'Shipment picked up',
                    },
                    {
                        'date': timezone.now() - timedelta(days=10, hours=18, minutes=30),
                        'location': f'{shipment.origin} Sorting Center',
                        'description': 'Shipment processed at sorting facility',
                    },
                    {
                        'date': timezone.now() - timedelta(days=9, hours=7, minutes=15),
                        'location': f'{shipment.origin} International Airport',
                        'description': 'Shipment departed from origin airport',
                    },
                    {
                        'date': timezone.now() - timedelta(days=7, hours=9, minutes=45),
                        'location': f'{shipment.destination} International Airport',
                        'description': 'Shipment arrived at destination airport',
                    },
                    {
                        'date': timezone.now() - timedelta(days=6, hours=14, minutes=30),
                        'location': f'{shipment.destination} Customs',
                        'description': 'Shipment cleared customs',
                    },
                    {
                        'date': timezone.now() - timedelta(days=5, hours=10, minutes=15),
                        'location': f'{shipment.destination} Distribution Center',
                        'description': 'Shipment out for delivery',
                    },
                    {
                        'date': timezone.now() - timedelta(days=5, hours=16, minutes=45),
                        'location': f'{shipment.destination}',
                        'description': 'Shipment delivered',
                    },
                ]
            elif shipment.status == 'Processing':
                events = [
                    {
                        'date': timezone.now() - timedelta(days=11, hours=11, minutes=20),
                        'location': 'Online',
                        'description': 'Shipping label created',
                    },
                    {
                        'date': timezone.now() - timedelta(days=10, hours=15, minutes=45),
                        'location': f'{shipment.origin}',
                        'description': 'Shipment picked up',
                    },
                ]
            else:  # Exception
                events = [
                    {
                        'date': timezone.now() - timedelta(days=12, hours=9, minutes=20),
                        'location': 'Online',
                        'description': 'Shipping label created',
                    },
                    {
                        'date': timezone.now() - timedelta(days=11, hours=13, minutes=45),
                        'location': f'{shipment.origin}',
                        'description': 'Shipment picked up',
                    },
                    {
                        'date': timezone.now() - timedelta(days=10, hours=17, minutes=30),
                        'location': f'{shipment.origin} Sorting Center',
                        'description': 'Shipment processed at sorting facility',
                    },
                    {
                        'date': timezone.now() - timedelta(days=9, hours=8, minutes=15),
                        'location': f'{shipment.origin} International Airport',
                        'description': 'Shipment departed from origin airport',
                    },
                    {
                        'date': timezone.now() - timedelta(days=7, hours=10, minutes=45),
                        'location': f'{shipment.destination} International Airport',
                        'description': 'Shipment arrived at destination airport',
                    },
                    {
                        'date': timezone.now() - timedelta(days=6, hours=9, minutes=30),
                        'location': f'{shipment.destination} Customs',
                        'description': 'Exception: Shipment held at customs',
                    },
                ]
            
            for event_data in events:
                TrackingEvent.objects.create(shipment=shipment, **event_data)
                self.stdout.write(f'  Created tracking event: {event_data["description"]}')
        
        # Create activities
        self.stdout.write('Creating activities...')
        activities = [
            {
                'user': 'Admin User',
                'action': 'created a new shipment',
                'target': created_shipments[0].id,
                'timestamp': timezone.now() - timedelta(minutes=5),
            },
            {
                'user': 'System',
                'action': 'updated status for shipment',
                'target': created_shipments[0].id,
                'timestamp': timezone.now() - timedelta(hours=1),
            },
            {
                'user': 'Admin User',
                'action': 'added a new customer',
                'target': 'Global Exports Ltd.',
                'timestamp': timezone.now() - timedelta(hours=3),
            },
            {
                'user': 'System',
                'action': 'flagged shipment with exception',
                'target': created_shipments[3].id,
                'timestamp': timezone.now() - timedelta(hours=5),
            },
        ]
        
        for activity_data in activities:
            Activity.objects.create(**activity_data)
            self.stdout.write(f'Created activity: {activity_data["user"]} {activity_data["action"]} {activity_data["target"]}')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
