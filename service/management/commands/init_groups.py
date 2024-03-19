# Inside management/commands/create_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates new permissions and assigns them to groups'

    def handle(self, *args, **options):

        # Get the content type
        content_type = ContentType.objects.get_for_model(Group)

        # Define the new permissions as tuples
        class NewPermissions:
            CAN_DELETE_ACCOUNT = ('can_delete_account', 'Can delete account')

        # Create the new permissions
        permission, _ = Permission.objects.get_or_create(
            codename=NewPermissions.CAN_DELETE_ACCOUNT[0],
            name=NewPermissions.CAN_DELETE_ACCOUNT[1],
            content_type=content_type
        )

        # Create groups
        client, _ = Group.objects.get_or_create(name='CLIENT')
        admin, _ = Group.objects.get_or_create(name='ADMIN')

        # Add permissions to groups
        client.permissions.add(permission)
        admin.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Permissions created successfully!'))
