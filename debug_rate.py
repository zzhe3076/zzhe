import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.db.models import Count, Q
from welcome_app.models import Student

# Simulate the view query
total = Student.objects.count()
checked_in = Student.objects.filter(status='checked_in').count()
pending = total - checked_in
check_in_rate = round(checked_in / total * 100, 1) if total > 0 else 0

print(f"Total: {total}")
print(f"Checked_in: {checked_in}")
print(f"Pending: {pending}")
print(f"Check-in rate: {check_in_rate}%")

# Show college stats
college_stats = list(
    Student.objects.values('major__college__name')
    .annotate(
        total=Count('id'),
        checked_in=Count('id', filter=Q(status='checked_in'))
    )
    .order_by('-total')[:10]
)

print("\nCollege stats:")
for cs in college_stats:
    name = cs.get('major__college__name', '未知')
    total_college = cs.get('total', 0)
    checked = cs.get('checked_in', 0)
    rate = round(checked / total_college * 100, 1) if total_college > 0 else 0
    print(f"  {name}: {checked}/{total_college} = {rate}%")
