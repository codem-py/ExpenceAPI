import re

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User
from rest_framework.fields import EmailField, IntegerField


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data.get("fullname", "")
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user


class RegisterCheckSerializer(Serializer):
    email = EmailField(required=True)
    code = IntegerField(required=True)

    def validate(self, data):
        verify_code = cache.get(data["email"])
        if not verify_code:
            raise ValidationError({"code": "Tasdiqlash kodi eskirgan yoki noto‘g‘ri!"})
        if str(data["code"]) != str(verify_code):
            raise ValidationError({"code": "Noto‘g‘ri kod!"})
        return data
