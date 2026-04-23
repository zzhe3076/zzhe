import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

response = client.get('/admin/')
print(f"Status: {response.status_code}")
print(f"Location: {response.get('Location', 'None')}")