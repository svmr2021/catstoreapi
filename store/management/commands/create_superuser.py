# Django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

# Settings chec

# User model
user_model = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = settings.SUPERUSER
        username = super_user['username']
        password = super_user['password']
        email = super_user['email']
        if not user_model.objects.filter(username=username).exists():
            print('Creating account for %s (%s)' % (username, email))
            admin = user_model.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print('Superuser created. Username - {}, Password - {}'.format(username, password))
