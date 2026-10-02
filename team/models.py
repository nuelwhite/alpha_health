from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import bleach
from core.models import Organization

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'h2', 'h3', 'h4',
                 'ul', 'ol', 'li', 'a', 'blockquote']
ALLOWED_ATTRS = {'a': ['href', 'title']}


class TeamMember(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='team_members',
    )
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    biography = CKEditor5Field(config_name='default', blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f'{self.name} — {self.position}'

    def save(self, *args, **kwargs):
        self.biography = bleach.clean(self.biography, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
        super().save(*args, **kwargs)
