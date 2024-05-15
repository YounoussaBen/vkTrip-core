from authentication.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        # Get the superuser's email and password
        admin_email = 'admin@vktrip.com'  # e.g., 'admin'
        admin_password = 'gSdsAjgH@F3Sdh'  # e.g., 'p@ssw0rd'
        
        # Check if a user with the admin_email exists, and if not, create a superuser
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password=admin_password
            )
        print(f'Superuser {admin_email} has been created.')
