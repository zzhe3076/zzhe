import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

# 测试 /admin/login/
response = client.get('/admin/login/')
print(f"URL: /admin/login/")
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
print(f"Content length: {len(response.content)}")
print(f"Has 'login' in content: {b'login' in response.content}")
print(f"Has 'Django' in content: {b'Django' in response.content}")
print(f"Has 'username' in content: {b'username' in response.content}")
print()

# 检查 /admin/ 是否重定向
response = client.get('/admin/')
print(f"URL: /admin/")
print(f"Status: {response.status_code}")
print(f"Redirect to: {response.get('Location')}")