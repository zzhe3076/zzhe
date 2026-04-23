import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.urls import reverse
from django.test import Client

# 测试 URL 路由
client = Client()

# 测试 Django 管理后台
response = client.get('/admin/')
print(f"Django admin status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response['Content-Type']}")

# 测试数据大屏
response = client.get('/')
print(f"\nHome page status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response['Content-Type']}")

# 测试学生管理页面
response = client.get('/students/')
print(f"\nStudents page status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response['Content-Type']}")

# 测试扫码报到页面
response = client.get('/checkin/')
print(f"\nCheckin page status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response['Content-Type']}")

# 测试 API
response = client.get('/api/students/')
print(f"\nAPI status: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response['Content-Type']}")