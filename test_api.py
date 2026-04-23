import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
sys.path.insert(0, r'd:\xinshen')
django.setup()

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from welcome_app.models import College, Major, Student

def create_test_data():
    print("=" * 50)
    print("Create test data...")
    print("=" * 50)

    college, _ = College.objects.get_or_create(
        name="计算机学院", 
        code="CS", 
        defaults={"description": "计算机科学与技术学院"}
    )
    print(f"[OK] College: {college.name}")

    major, _ = Major.objects.get_or_create(
        name="软件工程", 
        code="SE2024", 
        defaults={"college": college, "description": "软件工程专业"}
    )
    print(f"[OK] Major: {major.name}")

    user, _ = User.objects.get_or_create(username='student1', defaults={'email': 'student1@test.com'})
    if user.password == '':
        user.set_password('test123')
        user.save()
    student, _ = Student.objects.get_or_create(
        student_id="2024001",
        defaults={
            'user': user,
            'name': "张三",
            'gender': "male",
            'id_card': "110101200001011234",
            'phone': "13800138000",
            'major': major,
            'origin_province': "北京",
            'origin_city': "北京市",
            'high_school': "北京四中"
        }
    )
    print(f"[OK] Student: {student.name} ({student.student_id})")

    return college, major, student

def test_api():
    print("\n" + "=" * 50)
    print("API Testing...")
    print("=" * 50)

    client = APIClient()

    print("\n1. Test colleges API (GET /api/colleges/)")
    response = client.get('/api/colleges/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Data: {response.json()}")
        print("   [PASS] Colleges API")

    print("\n2. Test majors API (GET /api/majors/)")
    response = client.get('/api/majors/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Data: {response.json()}")
        print("   [PASS] Majors API")

    print("\n3. Test students API (GET /api/students/)")
    response = client.get('/api/students/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Count: {len(response.json()['results']) if 'results' in response.json() else len(response.json())}")
        print("   [PASS] Students API")

    print("\n4. Test dashboard API (GET /api/dashboard/stats/)")
    response = client.get('/api/dashboard/stats/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Student Stats: {data.get('student_stats', {})}")
        print("   [PASS] Dashboard API")

    print("\n5. Test knowledge-base search API (GET /api/knowledge-base/search/)")
    response = client.get('/api/knowledge-base/search/?q=报到')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Result: {response.json()}")
        print("   [PASS] Knowledge-base Search API")

    print("\n6. Test announcements API (GET /api/announcements/)")
    response = client.get('/api/announcements/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Data: {response.json()}")
        print("   [PASS] Announcements API")

    print("\n" + "=" * 50)
    print("All API tests completed!")
    print("=" * 50)

if __name__ == '__main__':
    create_test_data()
    test_api()
