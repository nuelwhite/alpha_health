from django.contrib import admin
from .models import Organization

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active', 'display_order')
    list_filter = ('active', 'country')
    prepopulated_fields = {'slug': ('name',)}
    