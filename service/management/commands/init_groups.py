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
        list_permissions_client = [
            ['can_buy_membership', 'Can buy membership']
        ]

        list_permissions_admin = [
            ['can_view_admin_panel', 'Can view admin panel'],
            ['can_delete_accounts', 'Can delete accounts'],
            ['can_edit_clients_profile', 'Can edit clients profile'],
        ]
            
        # Create/Select groups
        client, _ = Group.objects.get_or_create(name='CLIENT')
        admin, _ = Group.objects.get_or_create(name='ADMIN')

        # Create the new permissions (client)
        for perm in list_permissions_client:
            permission, _ = Permission.objects.get_or_create(
                codename= perm[0],
                name= perm[1],
                content_type= content_type
            )
            client.permissions.add(permission)
        
        # Create the new permissions (admin)
        for perm in list_permissions_admin:
            permission, _ = Permission.objects.get_or_create(
                codename= perm[0],
                name= perm[1],
                content_type= content_type
            )
            admin.permissions.add(permission)            

        self.stdout.write(self.style.SUCCESS('Permissions created successfully!'))
