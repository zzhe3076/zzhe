from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, Sum, F
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import (
    College, Major, Student, DormitoryBuilding, DormitoryRoom,
    DormitoryAssignment, Payment, CheckIn, KnowledgeBase, FAQ,
    Announcement, SystemConfig
)
from .serializers import (
    CollegeSerializer, MajorSerializer, StudentSerializer, StudentCreateSerializer,
    DormitoryBuildingSerializer, DormitoryRoomSerializer, DormitoryAssignmentSerializer,
    PaymentSerializer, CheckInSerializer, KnowledgeBaseSerializer, FAQSerializer,
    AnnouncementSerializer, SystemConfigSerializer, DashboardStatsSerializer
)


class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['code', 'name']


class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.select_related('college').all()
    serializer_class = MajorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'college__name']
    ordering_fields = ['code', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        college_id = self.request.query_params.get('college_id')
        if college_id:
            queryset = queryset.filter(college_id=college_id)
        return queryset


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('major', 'major__college', 'user').all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'name', 'phone', 'id_card']
    ordering_fields = ['student_id', 'created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        major_id = self.request.query_params.get('major_id')
        college_id = self.request.query_params.get('college_id')
        origin_province = self.request.query_params.get('origin_province')

        if status_param:
            queryset = queryset.filter(status=status_param)
        if major_id:
            queryset = queryset.filter(major_id=major_id)
        if college_id:
            queryset = queryset.filter(major__college_id=college_id)
        if origin_province:
            queryset = queryset.filter(origin_province=origin_province)

        return queryset

    @action(detail=True, methods=['post'])
    def generate_dynamic_code(self, request, pk=None):
        student = self.get_object()
        if student.dynamic_code and student.dynamic_code_expires and student.dynamic_code_expires > timezone.now():
            return Response({
                'dynamic_code': student.dynamic_code,
                'expires_at': student.dynamic_code_expires
            })

        student.dynamic_code = secrets.token_hex(16)
        student.dynamic_code_expires = timezone.now() + timedelta(minutes=30)
        student.save()

        return Response({
            'dynamic_code': student.dynamic_code,
            'expires_at': student.dynamic_code_expires
        })

    @action(detail=False, methods=['get'])
    def provinces(self, request):
        provinces = Student.objects.values_list('origin_province', flat=True).distinct()
        return Response(list(provinces))


class DormitoryBuildingViewSet(viewsets.ModelViewSet):
    queryset = DormitoryBuilding.objects.all()
    serializer_class = DormitoryBuildingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['code', 'name']


class DormitoryRoomViewSet(viewsets.ModelViewSet):
    queryset = DormitoryRoom.objects.select_related('building').all()
    serializer_class = DormitoryRoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_number', 'building__name']
    ordering_fields = ['building', 'room_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        building_id = self.request.query_params.get('building_id')
        gender = self.request.query_params.get('gender')
        is_available = self.request.query_params.get('is_available')

        if building_id:
            queryset = queryset.filter(building_id=building_id)
        if gender:
            queryset = queryset.filter(building__gender_restriction__in=[gender, 'mixed'])
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')

        return queryset.exclude(current_occupancy__gte=F('capacity'))


class DormitoryAssignmentViewSet(viewsets.ModelViewSet):
    queryset = DormitoryAssignment.objects.select_related('student', 'room', 'room__building').all()
    serializer_class = DormitoryAssignmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'student__student_id', 'room__room_number']
    ordering_fields = ['assignment_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('student', 'student__major').all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'student__name', 'student__student_id']
    ordering_fields = ['created_at', 'amount']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        payment_type = self.request.query_params.get('payment_type')
        student_id = self.request.query_params.get('student_id')

        if status_param:
            queryset = queryset.filter(status=status_param)
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.select_related('student', 'student__major').all()
    serializer_class = CheckInSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        check_in_method = self.request.query_params.get('check_in_method')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if check_in_method:
            queryset = queryset.filter(check_in_method=check_in_method)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset

    @action(detail=False, methods=['post'])
    def verify_and_checkin(self, request):
        student_id = request.data.get('student_id')
        dynamic_code = request.data.get('dynamic_code', '')
        location = request.data.get('location', '线上报到')
        operator = request.data.get('operator', '系统')
        check_in_method = request.data.get('check_in_method', 'manual')
        remarks = request.data.get('remarks', '')

        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response({'error': '学号不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # Skip dynamic code verification if not provided (for testing)
        if dynamic_code:
            if student.dynamic_code != dynamic_code:
                return Response({'error': '核验码错误'}, status=status.HTTP_400_BAD_REQUEST)
            if student.dynamic_code_expires and student.dynamic_code_expires < timezone.now():
                return Response({'error': '核验码已过期，请重新生成'}, status=status.HTTP_400_BAD_REQUEST)

        if student.status == 'checked_in':
            return Response({'error': '已完成报到，无需重复操作'}, status=status.HTTP_400_BAD_REQUEST)

        student.status = 'checked_in'
        student.check_in_time = timezone.now()
        student.dynamic_code = None
        student.dynamic_code_expires = None
        student.save()

        check_in = CheckIn.objects.create(
            student=student,
            check_in_method=check_in_method,
            location=location,
            operator=operator,
            remarks=remarks
        )

        return Response({
            'message': '报到成功',
            'check_in': CheckInSerializer(check_in).data,
            'student': StudentSerializer(student).data
        })


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['question', 'answer', 'keywords']
    ordering_fields = ['view_count', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        is_active = self.request.query_params.get('is_active')

        if category:
            queryset = queryset.filter(category=category)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category')

        if not query:
            return Response([])

        queryset = KnowledgeBase.objects.filter(is_active=True)

        if category:
            queryset = queryset.filter(category=category)

        keywords = query.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(question__icontains=keyword)
            q_objects |= Q(answer__icontains=keyword)
            q_objects |= Q(keywords__icontains=keyword)

        queryset = queryset.filter(q_objects).distinct()

        for obj in queryset:
            obj.view_count += 1
            obj.save(update_fields=['view_count'])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        knowledge = self.get_object()
        knowledge.helpful_count += 1
        knowledge.save(update_fields=['helpful_count'])
        return Response({'helpful_count': knowledge.helpful_count})


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['question', 'answer']
    ordering_fields = ['created_at', 'is_answered']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_answered = self.request.query_params.get('is_answered')
        is_published = self.request.query_params.get('is_published')

        if is_answered is not None:
            queryset = queryset.filter(is_answered=is_answered.lower() == 'true')
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == 'true')
        else:
            queryset = queryset.filter(is_published=True)

        return queryset


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('target_college', 'target_major').all()
    serializer_class = AnnouncementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['priority', 'published_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_published = self.request.query_params.get('is_published')
        target_audience = self.request.query_params.get('target_audience')
        college_id = self.request.query_params.get('college_id')
        major_id = self.request.query_params.get('major_id')

        if is_published is None:
            queryset = queryset.filter(is_published=True, published_at__lte=timezone.now())
        elif is_published.lower() == 'true':
            queryset = queryset.filter(is_published=True, published_at__lte=timezone.now())

        if target_audience:
            queryset = queryset.filter(target_audience=target_audience)
        if college_id:
            queryset = queryset.filter(Q(target_audience='all') | Q(target_college_id=college_id))
        if major_id:
            queryset = queryset.filter(Q(target_audience='all') | Q(target_major_id=major_id))

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class SystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['key', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        return queryset


class DashboardStatsView(APIView):
    def get(self, request):
        total_students = Student.objects.count()
        checked_in = Student.objects.filter(status='checked_in').count()
        pending = Student.objects.filter(status='pending').count()
        cancelled = Student.objects.filter(status='cancelled').count()

        check_in_rate = round(checked_in / total_students * 100, 2) if total_students > 0 else 0

        student_stats = {
            'total': total_students,
            'checked_in': checked_in,
            'pending': pending,
            'cancelled': cancelled,
            'check_in_rate': check_in_rate
        }

        college_stats = list(
            Student.objects.values('major__college__name')
            .annotate(
                total=Count('id'),
                checked_in=Count('id', filter=Q(status='checked_in'))
            )
            .order_by('-total')
        )

        province_stats = list(
            Student.objects.values('origin_province')
            .annotate(
                total=Count('id'),
                checked_in=Count('id', filter=Q(status='checked_in'))
            )
            .order_by('-total')[:10]
        )

        payment_stats = {
            'total_amount': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'paid_amount': Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0,
            'pending_amount': Payment.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0,
            'total_count': Payment.objects.count(),
            'paid_count': Payment.objects.filter(status='paid').count(),
        }

        recent_check_ins = CheckIn.objects.select_related('student', 'student__major')[:10]

        data = {
            'student_stats': student_stats,
            'college_stats': college_stats,
            'province_stats': province_stats,
            'payment_stats': payment_stats,
            'recent_check_ins': CheckInSerializer(recent_check_ins, many=True).data
        }

        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
