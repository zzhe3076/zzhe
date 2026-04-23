from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db import models
from datetime import timedelta
import secrets
import hashlib
import json

from .models import Student, Announcement, FAQ, Payment, DormitoryAssignment
from .serializers import StudentSerializer, AnnouncementSerializer, FAQSerializer
from .wechat_serializers import (
    WechatLoginSerializer, WechatUserInfoSerializer,
    WechatDashboardSerializer, GenerateCodeSerializer,
    VerifyCheckinSerializer
)


WECHAT_APPID = 'your_appid'
WECHAT_SECRET = 'your_secret'


class WechatLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WechatLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        try:
            import urllib.request
            import urllib.parse

            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={WECHAT_APPID}&secret={WECHAT_SECRET}&js_code={code}&grant_type=authorization_code'
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            if 'openid' in data:
                openid = data['openid']
                session_key = data.get('session_key', '')

                request.session['wechat_openid'] = openid
                request.session['wechat_session_key'] = session_key

                return Response({
                    'success': True,
                    'openid': openid,
                    'message': '微信登录成功'
                })
            else:
                return Response({
                    'success': False,
                    'error': data.get('errmsg', '微信登录失败')
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': f'微信登录失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WechatBindView(APIView):
    def post(self, request):
        openid = request.session.get('wechat_openid')
        if not openid:
            return Response({
                'success': False,
                'error': '请先进行微信授权登录'
            }, status=status.HTTP_401_BAD_REQUEST)

        student_id = request.data.get('student_id')
        password = request.data.get('password')

        if not student_id or not password:
            return Response({
                'success': False,
                'error': '请提供学号和密码'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(student_id=student_id)
            user = student.user

            if not user.check_password(password):
                return Response({
                    'success': False,
                    'error': '学号或密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            request.session['student_id'] = student.id
            request.session['student_name'] = student.name

            return Response({
                'success': True,
                'message': '绑定成功',
                'student': WechatUserInfoSerializer(student).data
            })

        except Student.DoesNotExist:
            return Response({
                'success': False,
                'error': '学号不存在'
            }, status=status.HTTP_404_NOT_FOUND)


class WechatDashboardView(APIView):
    def get(self, request):
        student_id = request.session.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'error': '未登录'
            }, status=status.HTTP_401_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'error': '学生信息不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        announcements = Announcement.objects.filter(
            is_published=True,
            published_at__lte=timezone.now()
        )[:5]

        faqs = FAQ.objects.filter(
            is_published=True,
            is_answered=True
        )[:5]

        payments = Payment.objects.filter(student=student)
        payment_count = payments.filter(status='paid').count()
        payment_pending_amount = payments.filter(status='pending').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

        dormitory_assignment = DormitoryAssignment.objects.filter(student=student).first()
        has_dormitory = dormitory_assignment is not None
        dormitory_info = None
        if dormitory_assignment:
            dormitory_info = {
                'building': dormitory_assignment.room.building.name,
                'room_number': dormitory_assignment.room.room_number,
                'bed_number': dormitory_assignment.bed_number,
                'status': dormitory_assignment.status
            }

        data = {
            'student': WechatUserInfoSerializer(student).data,
            'announcements': AnnouncementSerializer(announcements, many=True).data,
            'faqs': FAQSerializer(faqs, many=True).data,
            'payment_count': payment_count,
            'payment_pending_amount': str(payment_pending_amount),
            'has_dormitory': has_dormitory,
            'dormitory_info': dormitory_info
        }

        return Response({
            'success': True,
            'data': data
        })


class WechatGenerateCodeView(APIView):
    def post(self, request):
        student_id = request.session.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'error': '未登录'
            }, status=status.HTTP_401_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'error': '学生信息不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        if student.dynamic_code and student.dynamic_code_expires and student.dynamic_code_expires > timezone.now():
            return Response({
                'success': True,
                'dynamic_code': student.dynamic_code,
                'expires_at': student.dynamic_code_expires
            })

        student.dynamic_code = secrets.token_hex(16)
        student.dynamic_code_expires = timezone.now() + timedelta(minutes=30)
        student.save()

        return Response({
            'success': True,
            'dynamic_code': student.dynamic_code,
            'expires_at': student.dynamic_code_expires
        })


class WechatVerifyCheckinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCheckinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data['student_id']
        dynamic_code = serializer.validated_data['dynamic_code']
        location = serializer.validated_data.get('location', '小程序扫码')
        check_in_method = serializer.validated_data.get('check_in_method', 'qrcode')

        try:
            student = Student.objects.get(student_id=student_id, dynamic_code=dynamic_code)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'error': '学号或核验码无效'
            }, status=status.HTTP_400_BAD_REQUEST)

        if student.dynamic_code_expires and student.dynamic_code_expires < timezone.now():
            return Response({
                'success': False,
                'error': '核验码已过期，请重新生成'
            }, status=status.HTTP_400_BAD_REQUEST)

        if student.status == 'checked_in':
            return Response({
                'success': False,
                'error': '已完成报到，无需重复操作'
            })

        from .models import CheckIn

        student.status = 'checked_in'
        student.check_in_time = timezone.now()
        student.dynamic_code = None
        student.dynamic_code_expires = None
        student.save()

        check_in = CheckIn.objects.create(
            student=student,
            check_in_method=check_in_method,
            location=location,
            operator='小程序',
            remarks='小程序扫码报到'
        )

        return Response({
            'success': True,
            'message': '报到成功',
            'student': WechatUserInfoSerializer(student).data
        })


class WechatPaymentListView(APIView):
    def get(self, request):
        student_id = request.session.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'error': '未登录'
            }, status=status.HTTP_401_BAD_REQUEST)

        payments = Payment.objects.filter(student_id=student_id)
        
        return Response({
            'success': True,
            'data': [{
                'id': p.id,
                'payment_type': p.get_payment_type_display(),
                'amount': str(p.amount),
                'status': p.get_status_display(),
                'order_number': p.order_number,
                'paid_at': p.paid_at
            } for p in payments]
        })


class WechatDormitoryView(APIView):
    def get(self, request):
        student_id = request.session.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'error': '未登录'
            }, status=status.HTTP_401_BAD_REQUEST)

        assignment = DormitoryAssignment.objects.filter(student_id=student_id).first()

        if not assignment:
            return Response({
                'success': True,
                'has_dormitory': False,
                'message': '暂未分配宿舍'
            })

        return Response({
            'success': True,
            'has_dormitory': True,
            'data': {
                'building': assignment.room.building.name,
                'room_number': assignment.room.room_number,
                'bed_number': assignment.bed_number,
                'room_type': assignment.room.get_room_type_display(),
                'price': str(assignment.room.price),
                'current_occupancy': assignment.room.current_occupancy,
                'capacity': assignment.room.capacity,
                'status': assignment.get_status_display()
            }
        })


class WechatLogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({
            'success': True,
            'message': '退出成功'
        })
