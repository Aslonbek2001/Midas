from .models import ClientModel, VerificationCode
from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta, timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .logics_user import send_verification_email
import random


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')
    class Meta:
        model = ClientModel
        fields = ('username', 'phone', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = ClientModel(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        send_verification_email(user)
        return user
    
class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        try:
            user = ClientModel.objects.get(email=email)
            verification_code = VerificationCode.objects.get(user=user)
            verification_code.delete()
        except (ClientModel.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError({"detail": "User or verification code not found."})

        if verification_code.is_verified:
            raise serializers.ValidationError({"detail": "This email is already verified."})
        
        if verification_code.end_time > timezone.now():
            raise serializers.ValidationError({"detail": "A verification code has been sent."})

        return data
    
    def save(self, **kwargs):
        email = self.validated_data['email']
        user = ClientModel.objects.get(email=email)
        send_verification_email(user)
        return {"detail": "A new verification code has been sent."}
    


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id', 'username', 'email',  'first_name', 'last_name', 'rule', 'location', 'phone']
        read_only_fields = ['id',  'rule']  # 'rule' o'zgarishiga yo'l qo'ymaslik

    def validate_email(self, value):
        user = self.context['request'].user
        if ClientModel.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone(self, value):
        user = self.context['request'].user
        if ClientModel.objects.filter(phone=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    class Meta:
        model = ClientModel
        fields = ('email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def update(self, validated_data):
        email = validated_data['email']
        user = ClientModel.objects.get(email=email)
        user.set_password(validated_data['password'])
        user.save()
        return user



