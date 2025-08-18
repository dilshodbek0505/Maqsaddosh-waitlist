from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import OTPSendView, LoginView, RegisterView

urlpatterns = [
    path("auth/OTPSend/", OTPSendView.as_view(), name="otp-send"),
    path("auth/TokeRefresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/Login/", LoginView.as_view(), name="user-login"),
    path("auth/Register/", RegisterView.as_view(), name="user-register"),
    
]
