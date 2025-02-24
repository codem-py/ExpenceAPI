from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from apps.models import User
from apps.serializers import RegisterModelSerializer, RegisterCheckSerializer
from apps.tasks import send_email
from django.core.cache import cache

# Create your views here.

@extend_schema(tags=['auth'], request=RegisterModelSerializer)
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user and user.is_active:
            return JsonResponse({"status": 400, "message": "Email oldin ro'yxatdan o'tgan!"}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user:
                user = serializer.save()

            random_code = randint(10000, 99999)
            send_email.delay(email, random_code)
            cache.set(email, str(random_code), timeout=300)

            return JsonResponse({
                "status": 200,
                "message": "Tasdiqlash kodi jo'natildi!",
                "data": None
            }, status=HTTP_200_OK)

        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

@extend_schema(tags=['auth'], request=RegisterCheckSerializer)
class RegisterCheckAPIView(APIView):
    def post(self, request):
        serializer = RegisterCheckSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            User.objects.filter(email=email).update(is_active=True)
            cache.delete(email)  # Kodni o‘chirish
            return JsonResponse({"status": 200, "message": "Ro‘yxatdan o‘tish muvaffaqiyatli!"}, status=HTTP_200_OK)

        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


