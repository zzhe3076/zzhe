import os
import sys
import django
import random
from datetime import datetime, timedelta

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from welcome_app.models import Student, Major, CheckIn, DormitoryAssignment, DormitoryRoom
from django.contrib.auth.models import User

# Get majors
majors = Major.objects.all()
if not majors:
    print("No majors found! Please run init_data.py first.")
    exit()

# Get rooms
rooms = DormitoryRoom.objects.all()
if not rooms:
    print("No rooms found! Please run init_data.py first.")
    exit()

provinces = ['北京', '上海', '广东', '浙江', '江苏', '四川', '湖北', '湖南', '山东', '河南', '河北', '安徽', '福建', '陕西', '辽宁']
cities = ['市', '市', '市', '市', '县']
high_schools = ['第一中学', '第二中学', '实验中学', '外国语学校', '高级中学', '第一高级中学']

# Create students
students_data = [
    {'student_id': '2024001', 'name': '张三', 'gender': 'male', 'id_card': '110101200001011234', 'phone': '13800138001'},
    {'student_id': '2024002', 'name': '李四', 'gender': 'male', 'id_card': '310101200002021234', 'phone': '13800138002'},
    {'student_id': '2024003', 'name': '王五', 'gender': 'female', 'id_card': '440101200003031234', 'phone': '13800138003'},
    {'student_id': '2024004', 'name': '赵六', 'gender': 'female', 'id_card': '330101200004041234', 'phone': '13800138004'},
    {'student_id': '2024005', 'name': '钱七', 'gender': 'male', 'id_card': '320101200005051234', 'phone': '13800138005'},
    {'student_id': '2024006', 'name': '孙八', 'gender': 'male', 'id_card': '510101200006061234', 'phone': '13800138006'},
    {'student_id': '2024007', 'name': '周九', 'gender': 'female', 'id_card': '420101200007071234', 'phone': '13800138007'},
    {'student_id': '2024008', 'name': '吴十', 'gender': 'female', 'id_card': '430101200008081234', 'phone': '13800138008'},
    {'student_id': '2024009', 'name': '郑十一', 'gender': 'male', 'id_card': '370101200009091234', 'phone': '13800138009'},
    {'student_id': '2024010', 'name': '刘十二', 'gender': 'male', 'id_card': '410101200010101234', 'phone': '13800138010'},
    {'student_id': '2024011', 'name': '陈一', 'gender': 'female', 'id_card': '130101200011111234', 'phone': '13800138011'},
    {'student_id': '2024012', 'name': '杨二', 'gender': 'female', 'id_card': '340101200012121234', 'phone': '13800138012'},
    {'student_id': '2024013', 'name': '黄三', 'gender': 'male', 'id_card': '350101200013131234', 'phone': '13800138013'},
    {'student_id': '2024014', 'name': '周四', 'gender': 'male', 'id_card': '610101200014141234', 'phone': '13800138014'},
    {'student_id': '2024015', 'name': '吴五', 'gender': 'female', 'id_card': '210101200015151234', 'phone': '13800138015'},
]

created_count = 0
checked_in_count = 0

for data in students_data:
    if Student.objects.filter(student_id=data['student_id']).exists():
        continue
    
    major = random.choice(majors)
    province = random.choice(provinces)
    city = random.choice(provinces[:8]) + random.choice(cities)
    high_school = random.choice(high_schools)
    class_name = f"{major.name[:2]}班{random.randint(1, 3)}"
    
    student = Student.objects.create(
        student_id=data['student_id'],
        name=data['name'],
        gender=data['gender'],
        id_card=data['id_card'],
        phone=data['phone'],
        major=major,
        class_name=class_name,
        origin_province=province,
        origin_city=city,
        high_school=high_school,
        status='pending'
    )
    created_count += 1
    
    # 70% chance to check in
    if random.random() < 0.7:
        student.status = 'checked_in'
        student.check_in_time = datetime.now() - timedelta(days=random.randint(0, 7))
        student.save()
        checked_in_count += 1
        
        # Create check-in record
        CheckIn.objects.create(
            student=student,
            check_in_method=random.choice(['manual', 'qrcode']),
            location='报到点A',
            operator='管理员',
            remarks='正常报到'
        )
        
        # Assign dormitory
        available_rooms = [r for r in rooms if r.current_occupancy < r.capacity]
        if available_rooms:
            room = random.choice(available_rooms)
            bed_num = room.current_occupancy + 1
            DormitoryAssignment.objects.create(
                student=student,
                room=room,
                bed_number=bed_num
            )
            room.current_occupancy += 1
            room.save()

print(f"\n=== Test Data Created ===")
print(f"Students created: {created_count}")
print(f"Checked in: {checked_in_count}")
print(f"Pending: {created_count - checked_in_count}")
print(f"\nTotal students in database: {Student.objects.count()}")
print(f"Checked in: {Student.objects.filter(status='checked_in').count()}")
print(f"Pending: {Student.objects.filter(status='pending').count()}")
