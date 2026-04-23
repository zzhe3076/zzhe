import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

# 测试 /admin/ 路径
response = client.get('/admin/')
print(f"URL: /admin/")
print(f"Status: {response.status_code}")
print(f"Location header: {response.get('Location', 'None')}")
print(f"Content (first 500 chars): {response.content[:500]}")
print()

# 测试 /admin/login/ 路径
response = client.get('/admin/login/')
print(f"URL: /admin/login/")
print(f"Status: {response.status_code}")
print(f"Content (first 500 chars): {response.content[:500]}")
print()

# 测试 /admin/student/ 路径
response = client.get('/admin/welcome_app/student/')
print(f"URL: /admin/welcome_app/student/")
print(f"Status: {response.status_code}")
if response.status_code == 302:
    print(f"Location header: {response.get('Location', 'None')}")