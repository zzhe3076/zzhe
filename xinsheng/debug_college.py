import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from welcome_app.models import Student
from django.db.models import Count, Q

# Test college stats query
college_stats = list(
    Student.objects.values('major__college__name')
    .annotate(
        total=Count('id'),
        checked_in=Count('id', filter=Q(status='checked_in'))
    )
    .order_by('-total')[:10]
)

print("College Stats:")
for cs in college_stats:
    print(f"  {cs}")

# Check if major__college is null for any students
print("\nStudents with null major:")
null_major = Student.objects.filter(major__isnull=True).count()
print(f"  Count: {null_major}")

print("\nStudents with null major__college:")
null_college = Student.objects.filter(major__college__isnull=True).count()
print(f"  Count: {null_college}")

# Show some student details
print("\nSample students:")
for s in Student.objects.select_related('major', 'major__college').all()[:3]:
    print(f"  {s.name} - major: {s.major.name if s.major else 'None'} - college: {s.major.college.name if s.major and s.major.college else 'None'}")
