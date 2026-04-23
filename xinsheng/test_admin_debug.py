import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client, override_settings

client = Client()

# 测试 /admin/login/ 请求
print("=" * 50)
print("Testing /admin/login/")
print("=" * 50)

response = client.get('/admin/login/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
print(f"Content length: {response.get('Content-Length')}")
print(f"Cookies: {dict(client.cookies)}")

# 检查是否有重定向
if response.status_code in [301, 302, 303, 307, 308]:
    print(f"Redirect to: {response.get('Location')}")
else:
    # 检查内容
    content = response.content.decode('utf-8')
    print(f"Title: {response.get('title', 'N/A')[:100] if hasattr(response, 'get') else 'N/A'}")
    print(f"First 200 chars: {content[:200]}")
    print(f"Contains 'username': {'username' in content}")
    print(f"Contains 'password': {'password' in content}")
    print(f"Contains 'login': {'login' in content.lower()}")

print()
print("=" * 50)
print("Testing /admin/")
print("=" * 50)

response = client.get('/admin/')
print(f"Status: {response.status_code}")
if response.status_code in [301, 302, 303, 307, 308]:
    print(f"Redirect to: {response.get('Location')}")