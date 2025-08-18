from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.bot.models import SmsPenndingBot


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "image",
            "is_superuser",
            "is_staff",
            "region",
        )
    
class OTPSendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    deep_link = serializers.CharField(read_only=True, max_length=255)

    def create(self, validated_data):
        from uuid import uuid4

        token = uuid4()
        phone = validated_data.get("phone")

        deep_link = "https://t.me/maqsaddosh_support_bot?start={}".format(token)
        token_obj, created = SmsPenndingBot.objects.get_or_create(phone=phone, defaults={"uuid": token})

        if not created:
            token_obj.uuid = token
            token_obj.code = None
            token_obj.save()

        validated_data['deep_link'] = deep_link
        return validated_data

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=5)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        phone = validated_data['phone']
        code = validated_data['code']
        
        token_obj = SmsPenndingBot.objects.filter(phone=phone).first()
        if not (token_obj and token_obj.code == code):
            raise serializers.ValidationError({"msg": "Kod yoki telefon raqam to'g'ri kelmadi"})

        user = User.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError({"msg": "Foydalanuvchi topilmadi"})
        
        refresh = RefreshToken.for_user(user)
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(refresh.access_token)

        token_obj.delete()
        return validated_data

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=5)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=128)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        phone = validated_data['phone']
        code = validated_data['code']

        user = User.objects.filter(phone=phone).first()
        if user:
            raise serializers.ValidationError({"msg": "Bunday foydalanuvchi allaqachon mavjud"})
        
        token_obj = SmsPenndingBot.objects.filter(phone=phone).first()
        if not (token_obj and token_obj.code == code):
            raise serializers.ValidationError({"msg": "Kod yoki telefon raqam to'g'ri kelmadi"})
        
        user = User.objects.create(
            phone=phone,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            region=validated_data.get('region')
        )

        refresh = RefreshToken.for_user(user)
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(refresh.access_token)

        token_obj.delete()
        return validated_data
