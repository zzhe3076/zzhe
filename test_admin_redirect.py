import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

# 测试 /admin/ 路径
response = client.get('/admin/')
print(f"URL: /admin/")
print(f"Status code: {response.status_code}")
print(f"URL after redirect: {response.url if response.status_code in [301, 302] else 'No redirect'}")
print(f"Content type: {response.headers.get('Content-Type')}")
print()

# 测试 /admin/login/ 路径
response = client.get('/admin/login/')
print(f"URL: /admin/login/")
print(f"Status code: {response.status_code}")
print(f"Content type: {response.headers.get('Content-Type')}")
print()

# 测试 / 路径（数据大屏）
response = client.get('/')
print(f"URL: /")
print(f"Status code: {response.status_code}")
print(f"Content type: {response.headers.get('Content-Type')}")
print()

# 检查是否有其他 URL 配置问题
from django.urls import resolve

# 解析 /admin/ 路径
resolved = resolve('/admin/')
print(f"Resolved /admin/: {resolved.url_name}")
print(f"Resolved view: {resolved.func.__name__}")
print()

# 解析 / 路径
resolved = resolve('/')
print(f"Resolved /: {resolved.url_name}")
print(f"Resolved view: {resolved.func.__name__}")