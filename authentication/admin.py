from django.contrib import admin
from .models import UserProfile, LoginAttempt

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'last_login_time', 'last_login_ip')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'success', 'timestamp')
    list_filter = ('success', 'timestamp')
    search_fields = ('username', 'ip_address')
