import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
sys.path.insert(0, r'd:\xinshen')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_frontend():
    client = Client()
    
    # 登录管理员
    User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    client.login(username='admin', password='admin123')
    
    print("=" * 50)
    print("Web Pages Testing...")
    print("=" * 50)
    
    pages = [
        ('/', 'Home -> Admin Dashboard'),
        ('/checkin/', 'Check-in Page'),
        ('/students/', 'Students Management'),
    ]
    
    for url, name in pages:
        response = client.get(url)
        status = "PASS" if response.status_code == 200 else f"FAIL ({response.status_code})"
        print(f"{status:20} | {url:25} | {name}")
    
    print("=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == '__main__':
    test_frontend()
