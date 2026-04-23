import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from welcome_app.models import College, Major, DormitoryBuilding, DormitoryRoom

# Create Colleges
colleges = [
    {'name': '计算机学院', 'code': 'CS'},
    {'name': '软件学院', 'code': 'SE'},
    {'name': '信息工程学院', 'code': 'IE'},
    {'name': '机械工程学院', 'code': 'ME'},
    {'name': '经济管理学院', 'code': 'EM'},
]

for c in colleges:
    College.objects.get_or_create(code=c['code'], defaults={'name': c['name']})

print('Colleges created!')

# Create Majors
majors = [
    {'name': '计算机科学与技术', 'code': 'CS001', 'college': 'CS'},
    {'name': '软件工程', 'code': 'SE001', 'college': 'SE'},
    {'name': '人工智能', 'code': 'AI001', 'college': 'CS'},
    {'name': '数据科学与大数据技术', 'code': 'DS001', 'college': 'IE'},
    {'name': '机械设计制造及其自动化', 'code': 'ME001', 'college': 'ME'},
    {'name': '工商管理', 'code': 'BA001', 'college': 'EM'},
    {'name': '会计学', 'code': 'AC001', 'college': 'EM'},
]

for m in majors:
    college = College.objects.get(code=m['college'])
    Major.objects.get_or_create(code=m['code'], defaults={'name': m['name'], 'college': college})

print('Majors created!')

# Create Dormitory Buildings
buildings = [
    {'name': '1号楼', 'code': 'B1', 'floor_count': 6, 'total_rooms': 120, 'available_rooms': 120},
    {'name': '2号楼', 'code': 'B2', 'floor_count': 6, 'total_rooms': 120, 'available_rooms': 120},
    {'name': '3号楼', 'code': 'B3', 'floor_count': 8, 'total_rooms': 160, 'available_rooms': 160},
]

for b in buildings:
    DormitoryBuilding.objects.get_or_create(code=b['code'], defaults={
        'name': b['name'],
        'floor_count': b['floor_count'],
        'total_rooms': b['total_rooms'],
        'available_rooms': b['available_rooms'],
    })

print('Dormitory buildings created!')

# Create some rooms
building = DormitoryBuilding.objects.first()
if building:
    for floor in range(1, building.floor_count + 1):
        for room_num in range(1, 11):
            room_code = f"{floor:02d}{room_num:02d}"
            DormitoryRoom.objects.get_or_create(
                building=building,
                room_number=room_code,
                defaults={
                    'floor': floor, 
                    'capacity': 4, 
                    'current_occupancy': 0,
                    'price': 1200
                }
            )

print('Dormitory rooms created!')

print('\n=== Initial data created successfully! ===')
