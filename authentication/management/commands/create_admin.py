from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile

class Command(BaseCommand):
    help = 'Creates a default admin user'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            return
        
        # Create admin user
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create admin profile
        UserProfile.objects.create(
            user=admin,
            role='admin'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        self.stdout.write(self.style.SUCCESS('Username: admin'))
        self.stdout.write(self.style.SUCCESS('Password: admin123'))
        self.stdout.write(self.style.WARNING('Please change the password after first login!'))
