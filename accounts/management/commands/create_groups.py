from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product

from orders.models import Order


class Command(BaseCommand):
    help = "Creates user groups and assigns permissions"

    def handle(self, *args, **kwargs):
        # Create or get the "Managers" group
        managers_group, created = Group.objects.get_or_create(name="Managers")
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Managers" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Group "Managers" already exists.'))

        self.assign_permissions(managers_group, Product,
                                ["add_product", "change_product", "delete_product", "view_product"])

        self.assign_permissions(managers_group, Order, ["view_order"])

        self.stdout.write(self.style.SUCCESS('Permissions assigned successfully to the "Managers" group.'))

        # Create or get the "Administrators" group
        admins_group, created = Group.objects.get_or_create(name="Administrators")
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Administrators" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Group "Administrators" already exists.'))

        # Give full access to Administrators group
        admins_group.permissions.set(Permission.objects.all())  # Full permissions
        self.stdout.write(self.style.SUCCESS('Group "Administrators" created with full access.'))

    def assign_permissions(self, group: Group, model, codenames: list[str]) -> None:
        """Assigns specific permissions to a given group."""
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=codenames
        )
        # Add permissions to the group (do not overwrite existing permissions)
        group.permissions.add(*permissions)
        self.stdout.write(self.style.SUCCESS(f'Permissions for {model.__name__} added to "Managers" group.'))

