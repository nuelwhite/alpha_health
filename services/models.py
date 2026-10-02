from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import bleach
from core.models import Organization

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'h2', 'h3', 'h4',
                 'ul', 'ol', 'li', 'a', 'blockquote']
ALLOWED_ATTRS = {'a': ['href', 'title']}


class Service(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='services',
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(blank=True)
    description = CKEditor5Field(config_name='default', blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = bleach.clean(self.description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
        super().save(*args, **kwargs)
