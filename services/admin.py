from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Service


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(config_name='default'),
        }


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ('name', 'organization', 'active', 'display_order')
    list_filter = ('active', 'organization')
    prepopulated_fields = {'slug': ('name',)}
