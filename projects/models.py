from django.db import models
from  core.models import Organization

# Create your models here.

class Project(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='projects',
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-project_date', '-created_at']

    def __str__(self):
        return self.title