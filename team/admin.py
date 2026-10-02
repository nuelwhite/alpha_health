from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import TeamMember


class TeamMemberAdminForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'biography': CKEditor5Widget(config_name='default'),
        }


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    form = TeamMemberAdminForm
    list_display = ('name', 'position', 'organization', 'active', 'display_order')
    list_filter = ('active', 'organization')
