import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.test import Client

client = Client()

# 测试所有相关 URL
urls = ['/admin/login/', '/admin/', '/', '/students/', '/checkin/']

for url in urls:
    response = client.get(url)
    content = response.content.decode('utf-8')[:300]
    print(f"URL: {url}")
    print(f"Status: {response.status_code}")
    print(f"Content preview: {content[:200]}")
    print("-" * 50)