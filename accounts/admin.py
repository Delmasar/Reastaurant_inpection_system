from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Restaurant

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_restaurant_owner', 'is_inspector', 'is_customer')
    list_filter = ('is_restaurant_owner', 'is_inspector', 'is_customer')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_restaurant_owner', 'is_inspector', 'is_customer')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Restaurant)