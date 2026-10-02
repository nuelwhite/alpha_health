from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Project, ProjectImage


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default'),
        }


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'organization', 'published', 'project_date')
    list_filter = ('published', 'organization')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
