from django.contrib import admin
from .models import InspectionRequest, Inspection

class InspectionRequestAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'requested_date', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('restaurant__name',)

class InspectionAdmin(admin.ModelAdmin):
    list_display = ('inspection_request', 'inspector', 'inspection_date', 'overall_rating')
    list_filter = ('inspector',)
    search_fields = ('inspection_request__restaurant__name',)

admin.site.register(InspectionRequest, InspectionRequestAdmin)
admin.site.register(Inspection, InspectionAdmin)