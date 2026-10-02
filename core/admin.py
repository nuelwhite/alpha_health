from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Organization, Redirect


class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(config_name='default'),
        }


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationAdminForm
    list_display = ('name', 'country', 'active', 'display_order')
    list_filter = ('active', 'country')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'created_at')
