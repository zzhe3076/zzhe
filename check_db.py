import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
sys.path.insert(0, r'd:\xinshen')
django.setup()

from django.db import connection
from welcome_app.models import Student, College, Major

print('=== 数据库连接状态 ===')
print(f'数据库引擎: {connection.vendor}')
print(f'数据库名称: {connection.settings_dict["NAME"]}')

print('\n=== 数据统计 ===')
print(f'学院数量: {College.objects.count()}')
print(f'专业数量: {Major.objects.count()}')
print(f'学生数量: {Student.objects.count()}')

print('\n=== 学生列表 ===')
for s in Student.objects.all()[:5]:
    print(f'- {s.name} ({s.student_id}) - {s.major.name if s.major else "未分配"}')
