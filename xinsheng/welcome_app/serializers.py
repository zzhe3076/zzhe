from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    College, Major, Student, DormitoryBuilding, DormitoryRoom,
    DormitoryAssignment, Payment, CheckIn, KnowledgeBase, FAQ,
    Announcement, SystemConfig
)


class CollegeSerializer(serializers.ModelSerializer):
    major_count = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = ['id', 'name', 'code', 'description', 'major_count', 'created_at', 'updated_at']

    def get_major_count(self, obj):
        return obj.majors.count()


class MajorSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)

    class Meta:
        model = Major
        fields = ['id', 'name', 'code', 'college', 'college_name', 'description', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    major_name = serializers.CharField(source='major.name', read_only=True)
    college_name = serializers.CharField(source='major.college.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'name', 'gender', 'gender_display', 'id_card', 'phone',
            'major', 'major_name', 'college_name', 'class_name', 'origin_province',
            'origin_city', 'high_school', 'status', 'status_display', 'check_in_time',
            'dynamic_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['dynamic_code', 'check_in_time']


class StudentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = [
            'username', 'password', 'student_id', 'name', 'gender', 'id_card',
            'phone', 'major', 'class_name', 'origin_province', 'origin_city', 'high_school'
        ]

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        
        # 如果没有提供username，使用student_id
        if not username:
            username = validated_data.get('student_id')
        
        # 创建用户账号
        if username and password:
            user = User.objects.create_user(username=username, password=password)
        else:
            user = None
        
        student = Student.objects.create(user=user, **validated_data)
        return student


class DormitoryBuildingSerializer(serializers.ModelSerializer):
    occupancy_rate = serializers.SerializerMethodField()

    class Meta:
        model = DormitoryBuilding
        fields = ['id', 'name', 'code', 'floor_count', 'total_rooms', 'available_rooms', 'gender_restriction', 'occupancy_rate']

    def get_occupancy_rate(self, obj):
        if obj.total_rooms > 0:
            return round((obj.total_rooms - obj.available_rooms) / obj.total_rooms * 100, 2)
        return 0


class DormitoryRoomSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)
    available_beds = serializers.SerializerMethodField()

    class Meta:
        model = DormitoryRoom
        fields = [
            'id', 'building', 'building_name', 'room_number', 'floor', 'capacity',
            'current_occupancy', 'available_beds', 'room_type', 'price', 'is_available'
        ]

    def get_available_beds(self, obj):
        return obj.capacity - obj.current_occupancy


class DormitoryAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    room_info = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DormitoryAssignment
        fields = ['id', 'student', 'student_name', 'student_id', 'room', 'room_info', 'bed_number', 'status', 'status_display', 'assignment_date']

    def get_room_info(self, obj):
        return f"{obj.room.building.name} - {obj.room.room_number}"


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'student', 'student_name', 'student_id', 'payment_type', 'payment_type_display',
            'amount', 'status', 'status_display', 'order_number', 'payment_method',
            'paid_at', 'transaction_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'paid_at', 'transaction_id']


class CheckInSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    check_in_method_display = serializers.CharField(source='get_check_in_method_display', read_only=True)

    class Meta:
        model = CheckIn
        fields = [
            'id', 'student', 'student_name', 'student_id', 'check_in_method',
            'check_in_method_display', 'location', 'operator', 'remarks', 'created_at'
        ]


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = KnowledgeBase
        fields = [
            'id', 'question', 'answer', 'category', 'category_display', 'keywords',
            'is_active', 'view_count', 'helpful_count', 'created_at', 'updated_at'
        ]


class FAQSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'student', 'student_name', 'question', 'answer', 'is_answered', 'is_published', 'created_at', 'answered_at']

    def get_student_name(self, obj):
        return obj.student.name if obj.student else None


class AnnouncementSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    target_audience_display = serializers.CharField(source='get_target_audience_display', read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'priority', 'priority_display', 'target_audience',
            'target_audience_display', 'target_college', 'target_major', 'is_published',
            'published_at', 'expires_at', 'created_at', 'updated_at'
        ]


class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'is_public', 'created_at', 'updated_at']


class StudentStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    checked_in = serializers.IntegerField()
    pending = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    check_in_rate = serializers.FloatField()


class DashboardStatsSerializer(serializers.Serializer):
    student_stats = StudentStatsSerializer()
    college_stats = serializers.ListField()
    province_stats = serializers.ListField()
    payment_stats = serializers.DictField()
    recent_check_ins = CheckInSerializer(many=True)
