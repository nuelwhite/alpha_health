from django.contrib import admin
from .models import Organization, Redirect


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active', 'display_order')
    list_filter = ('active', 'country')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'created_at')
