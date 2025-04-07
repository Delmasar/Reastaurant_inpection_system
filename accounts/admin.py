from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Restaurant

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_restaurant_owner', 'is_inspector')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_restaurant_owner', 'is_inspector')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Restaurant)