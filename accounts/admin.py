from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'location', 'created_at']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['created_at']
