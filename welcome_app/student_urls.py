from django.urls import path
from .student_views import (
    StudentLoginView,
    StudentDashboardView,
    StudentDormitoryView,
    StudentPaymentView,
    StudentAnnouncementView,
    StudentFAQView,
    StudentLogoutView
)

urlpatterns = [
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('student/logout/', StudentLogoutView.as_view(), name='student-logout'),
    path('student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('student/dormitory/', StudentDormitoryView.as_view(), name='student-dormitory'),
    path('student/payment/', StudentPaymentView.as_view(), name='student-payment'),
    path('student/announcement/', StudentAnnouncementView.as_view(), name='student-announcement'),
    path('student/faq/', StudentFAQView.as_view(), name='student-faq'),
]
