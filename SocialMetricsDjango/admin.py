from django.contrib import admin
from . import models
# Register your models here.
class ServiceRequestAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

admin.site.register(models.ServiceRequest, ServiceRequestAdmin)
