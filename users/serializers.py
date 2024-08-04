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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

ClientModel = get_user_model()


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


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        try:
            user = ClientModel.objects.get(email=email)
        except ClientModel.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found."})
        
        send_verification_email(user)
        return {"detail": "A new verification code has been sent."}
    


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id', 'username', 'email',  'first_name', 'last_name', 'rule', 'location', 'phone']
        read_only_fields = ['id',  'rule'] 

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


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords must match."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm new password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Hozirgi parol noto'g'ri.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Yangi parollar mos kelmayapti."})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        update_last_login(None, user)
        return user