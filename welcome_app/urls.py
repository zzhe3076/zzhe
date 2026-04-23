from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CollegeViewSet, MajorViewSet, StudentViewSet,
    DormitoryBuildingViewSet, DormitoryRoomViewSet,
    DormitoryAssignmentViewSet, PaymentViewSet, CheckInViewSet,
    KnowledgeBaseViewSet, FAQViewSet, AnnouncementViewSet,
    SystemConfigViewSet, DashboardStatsView
)

router = DefaultRouter()
router.register(r'colleges', CollegeViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'dormitory-buildings', DormitoryBuildingViewSet)
router.register(r'dormitory-rooms', DormitoryRoomViewSet)
router.register(r'dormitory-assignments', DormitoryAssignmentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'check-ins', CheckInViewSet)
router.register(r'knowledge-base', KnowledgeBaseViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'system-configs', SystemConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
