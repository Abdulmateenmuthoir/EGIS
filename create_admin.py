import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileregistry.settings')
django.setup()

from core.models import User

if not User.objects.filter(email='admin@egis.com').exists():
    u = User.objects.create_superuser(
        email='admin@egis.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print(f'Superuser created: {u.email}')
else:
    print('Superuser already exists.')
