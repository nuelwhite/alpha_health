from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    website_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['display_order', 'name']
 
        
class Redirect(models.Model):
    old_path = models.CharField(max_length=255, unique=True, help_text='e.g. /projects/old-slug/')
    new_path = models.CharField(max_length=255, help_text='e.g. /projects/new-slug/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.old_path} → {self.new_path}'       

    
    