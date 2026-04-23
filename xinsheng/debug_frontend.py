import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from welcome_app.models import Student

# 测试 Student 模型查询
total = Student.objects.count()
checked_in = Student.objects.filter(status='checked_in').count()
pending = total - checked_in

print(f"Total students: {total}")
print(f"Checked in: {checked_in}")
print(f"Pending: {pending}")

# 检查所有学生的状态
students = Student.objects.all()
print("\nAll students:")
for student in students:
    print(f"{student.student_id} - {student.name} - {student.status}")

# 检查学院统计
from django.db.models import Count, Q
college_stats = list(
    Student.objects.values('major__college__name')
    .annotate(
        total=Count('id'),
        checked_in=Count('id', filter=Q(status='checked_in'))
    )
    .order_by('-total')[:10]
)

print("\nCollege stats:")
for college in college_stats:
    print(college)