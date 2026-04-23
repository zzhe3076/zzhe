from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student


class WechatLoginSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=128, required=True, help_text="wx.login返回的code")
    encryptedData = serializers.CharField(required=False, help_text="encryptedData")
    iv = serializers.CharField(required=False, help_text="iv")


class WechatUserInfoSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=20)
    major_name = serializers.CharField(max_length=100)
    college_name = serializers.CharField(max_length=100)
    class_name = serializers.CharField(max_length=50, allow_blank=True)
    origin_province = serializers.CharField(max_length=50)
    origin_city = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.CharField(max_length=20)
    status_display = serializers.CharField()
    check_in_time = serializers.DateTimeField(allow_null=True)


class WechatDashboardSerializer(serializers.Serializer):
    student = WechatUserInfoSerializer()
    announcements = serializers.ListField()
    faqs = serializers.ListField()
    payment_count = serializers.IntegerField()
    payment_pending_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    has_dormitory = serializers.BooleanField()
    dormitory_info = serializers.DictField(allow_null=True)


class GenerateCodeSerializer(serializers.Serializer):
    pass


class VerifyCheckinSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=20)
    dynamic_code = serializers.CharField(max_length=32)
    location = serializers.CharField(max_length=100, required=False, default="小程序扫码")
    check_in_method = serializers.CharField(max_length=20, required=False, default="qrcode")
