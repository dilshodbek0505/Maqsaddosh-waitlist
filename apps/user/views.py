from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import get_user_model
from apps.user.serializers import OTPSendSerializer, LoginSerializer, RegisterSerializer

User = get_user_model()


class OTPSendView(CreateAPIView):
    serializer_class = OTPSendSerializer
    permission_classes = [AllowAny]

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

