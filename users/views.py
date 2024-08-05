from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import ClientModel, VerificationCode
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer, 
    VerifyCodeSerializer, 
    SendVerificationCodeSerializer,
    ResetPasswordSerializer,
    ClientProfileSerializer, ChangePasswordSerializer
    )
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .logics_user import send_verification_email
from drf_spectacular.utils import extend_schema, OpenApiResponse


####################  Registration     ##########################
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

####################  Verify Code     ##########################
class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = ClientModel.objects.get(email=email)
            verification_code = VerificationCode.objects.filter(user=user).order_by('-id').first()
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


####################  Send Verification Code  ##########################
class SendVerificationCodeView(generics.GenericAPIView):
    serializer_class = SendVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(message, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(
                response=None,
                description='Password updated successfully'
            ),
            400: OpenApiResponse(
                response=None,
                description='Validation error: Passwords do not match or other input issues'
            )
        }
    )
    
    def put(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {'request': self.request}


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(
                response=ChangePasswordSerializer,
                description='Password changed successfully.'
            ),
            400: OpenApiResponse(
                response=None,
                description='Error: Invalid login information.'
            )
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)