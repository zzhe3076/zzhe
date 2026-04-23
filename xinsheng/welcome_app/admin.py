from django.contrib import admin
from .models import (
    College, Major, Student, DormitoryBuilding, 
    DormitoryRoom, DormitoryAssignment, Payment, 
    CheckIn, KnowledgeBase, FAQ, Announcement, SystemConfig
)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'college', 'created_at')
    list_filter = ('college',)
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'major', 'gender', 'phone', 'status')
    list_filter = ('gender', 'major__college', 'status')
    search_fields = ('student_id', 'name', 'phone', 'id_card')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DormitoryBuilding)
class DormitoryBuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'gender_restriction', 'total_rooms', 'available_rooms')
    list_filter = ('gender_restriction',)
    search_fields = ('name', 'code')

@admin.register(DormitoryRoom)
class DormitoryRoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building', 'floor', 'capacity', 'current_occupancy', 'price')
    list_filter = ('building', 'floor')
    search_fields = ('room_number', 'building__name')

@admin.register(DormitoryAssignment)
class DormitoryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'bed_number', 'status', 'assignment_date')
    list_filter = ('status', 'room__building')
    search_fields = ('student__name', 'student__student_id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'payment_type', 'amount', 'status', 'paid_at')
    list_filter = ('payment_type', 'status')
    search_fields = ('student__name', 'student__student_id', 'order_number')
    readonly_fields = ('created_at',)

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('student', 'check_in_method', 'location', 'operator', 'created_at')
    list_filter = ('check_in_method',)
    search_fields = ('student__name', 'student__student_id')
    readonly_fields = ('created_at',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'view_count', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_answered', 'is_published', 'created_at')
    list_filter = ('is_answered', 'is_published')
    search_fields = ('question', 'answer')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_published', 'target_audience', 'created_at')
    list_filter = ('priority', 'is_published', 'target_audience')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    search_fields = ('key', 'value')
