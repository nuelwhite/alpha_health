from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

FULL = ['add', 'change', 'delete', 'view']
EDIT = ['change', 'view']
VIEW = ['view']

CONTENT_MODELS = [
    ('projects', 'project'),
    ('projects', 'projectimage'),
    ('services', 'service'),
    ('team', 'teammember'),
    ('core', 'organization'),
    ('core', 'redirect'),
    ('products', 'productcategory'),
    ('products', 'product'),
    ('contact', 'contactinquiry'),
]

ROLES = {
    'Content Manager': [
        ('projects', 'project', FULL),
        ('projects', 'projectimage', FULL),
        ('services', 'service', FULL),
        ('team', 'teammember', FULL),
        ('core', 'organization', EDIT),
        ('core', 'redirect', FULL),
    ],
    'Product Manager': [
        ('products', 'productcategory', FULL),
        ('products', 'product', FULL),
    ],
    'Inquiry Handler': [
        ('contact', 'contactinquiry', EDIT),
    ],
    'Read Only': [(app, model, VIEW) for app, model in CONTENT_MODELS],
}


class Command(BaseCommand):
    help = 'Create or reset the standard staff role groups and their permissions.'

    def handle(self, *args, **options):
        for role, grants in ROLES.items():
            group, created = Group.objects.get_or_create(name=role)
            perms = []
            for app_label, model, actions in grants:
                for action in actions:
                    perms.append(Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=f'{action}_{model}',
                    ))
            group.permissions.set(perms)
            verb = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{verb} {role} ({len(perms)} permissions)'))
