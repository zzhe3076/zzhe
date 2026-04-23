import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

# 测试 /admin/login/
response = client.get('/admin/login/')
print(f"/admin/login/ -> Status: {response.status_code}")
print(f"Contains 'username': {b'username' in response.content}")
print(f"Contains 'Django': {b'Django' in response.content}")

# 测试 /
response = client.get('/')
print(f"/ -> Status: {response.status_code}")
print(f"Contains '数据大屏': {'数据大屏' in response.content.decode('utf-8')}")