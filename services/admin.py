from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'active', 'display_order')
    list_filter = ('active', 'organization')
    prepopulated_fields = {'slug': ('name',)}