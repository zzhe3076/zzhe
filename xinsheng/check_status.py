import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from welcome_app.models import Student
from django.db.models import Count

print('Total students:', Student.objects.count())

status_counts = Student.objects.values('status').annotate(count=Count('id'))
for s in status_counts:
    print(f"Status: {s['status']}, Count: {s['count']}")

# Check first few students
print('\nFirst 5 students:')
for student in Student.objects.all()[:5]:
    print(f"  {student.student_id} - {student.name} - status: {student.status}")
