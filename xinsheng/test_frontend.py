import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
sys.path.insert(0, r'd:\xinshen')
django.setup()

from django.test import Client

def test_frontend():
    client = Client()
    
    print("=" * 50)
    print("Frontend Pages Testing...")
    print("=" * 50)
    
    pages = [
        ('/', 'Home Page'),
        ('/student/', 'Student Home'),
        ('/student/login/', 'Student Login'),
        ('/student/register/', 'Student Register'),
        ('/admin/', 'Admin Dashboard'),
        ('/admin/checkin/', 'Admin Check-in'),
        ('/admin/students/', 'Admin Students'),
    ]
    
    for url, name in pages:
        response = client.get(url)
        status = "PASS" if response.status_code == 200 else "FAIL"
        print(f"{status:6} | {url:30} | {name:20} | Status: {response.status_code}")
    
    print("=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == '__main__':
    test_frontend()
