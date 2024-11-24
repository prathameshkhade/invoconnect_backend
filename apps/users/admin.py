from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'user_type', 'business_name', 'is_verified', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'business_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Business Information', {
            'fields': ('business_name', 'business_type', 'phone', 'address', 'tax_number'),
            'classes': ('collapse',),
            'description': 'These fields are only relevant for Business Owner accounts.'
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('email', 'business_name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)