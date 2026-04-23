from django.urls import path
from .wechat_views import (
    WechatLoginView,
    WechatBindView,
    WechatDashboardView,
    WechatGenerateCodeView,
    WechatVerifyCheckinView,
    WechatPaymentListView,
    WechatDormitoryView,
    WechatLogoutView
)

urlpatterns = [
    path('wechat/login/', WechatLoginView.as_view(), name='wechat-login'),
    path('wechat/bind/', WechatBindView.as_view(), name='wechat-bind'),
    path('wechat/dashboard/', WechatDashboardView.as_view(), name='wechat-dashboard'),
    path('wechat/generate_code/', WechatGenerateCodeView.as_view(), name='wechat-generate-code'),
    path('wechat/verify_checkin/', WechatVerifyCheckinView.as_view(), name='wechat-verify-checkin'),
    path('wechat/payments/', WechatPaymentListView.as_view(), name='wechat-payments'),
    path('wechat/dormitory/', WechatDormitoryView.as_view(), name='wechat-dormitory'),
    path('wechat/logout/', WechatLogoutView.as_view(), name='wechat-logout'),
]
