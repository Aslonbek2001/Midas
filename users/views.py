from django.shortcuts import render
from rest_framework import serializers, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import ClientModel, VerificationCode
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer, 
    VerifyCodeSerializer, 
    ResendVerificationCodeSerializer,
    ResetPasswordSerializer,
    ClientProfileSerializer
    )
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .logics_user import send_verification_email


class RegisterView(generics.CreateAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserRegistrationSerializer(user).data,
            # "refresh": str(refresh),
            # "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = ClientModel.objects.get(email=email)
            verification_code = VerificationCode.objects.get(user=user, code=code)
        except (ClientModel.DoesNotExist, VerificationCode.DoesNotExist):
            return Response({"detail": "Invalid email or verification code."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the code is not expired (5 minutes)
        if timezone.now() > verification_code.end_time:
            return Response({"detail": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if verification_code.is_verified:
            return Response({"detail": "This code has already been used."}, status=status.HTTP_400_BAD_REQUEST)

        verification_code.is_verified = True
        verification_code.save()
        

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ResendVerificationCodeView(generics.GenericAPIView):
    serializer_class = ResendVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(message, status=status.HTTP_200_OK)


class ResendPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(message, status=status.HTTP_200_OK)


class ClientProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {'request': self.request}
