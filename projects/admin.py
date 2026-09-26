from django.contrib import admin
from .models import Project, ProjectImage

# Register your models here.

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'published', 'project_date')
    list_filter = ('published', 'organization')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]