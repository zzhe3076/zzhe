from django.urls import path
from .frontend_views import AdminIndexView, AdminCheckinView, AdminStudentsView

urlpatterns = [
    path('', AdminIndexView.as_view(), name='home'),
    path('checkin/', AdminCheckinView.as_view(), name='admin-checkin'),
    path('students/', AdminStudentsView.as_view(), name='admin-students'),
]
