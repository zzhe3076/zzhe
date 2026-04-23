import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.contrib.auth.models import User

user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com'}
)
user.set_password('admin123')
user.is_superuser = True
user.is_staff = True
user.save()

print('=' * 40)
print('Django Admin Login Info:')
print('=' * 40)
print('Username: admin')
print('Password: admin123')
print('URL: http://127.0.0.1:8000/admin/')
print('=' * 40)
