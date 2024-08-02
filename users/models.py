from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, datetime
from django.utils import timezone


class ClientModel(AbstractUser):
    class UserRule(models.TextChoices):
        ORDINARY = 'OU', 'Ordinary'
        ADMIN = 'AU', 'Admin'

    rule = models.CharField(
        max_length=2,
        choices=UserRule,
        default=UserRule.ORDINARY
    )

    email = models.EmailField(unique=True, db_index=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    location = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(verbose_name="Client phone", db_index=True, max_length=20, unique=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.phone}"
    
class VerificationCode(models.Model):
    user = models.OneToOneField(ClientModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.end_time:
    #         self.end_time = self.created_at + timedelta(minutes=5)
    #     super(VerificationCode, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.end_time:
            self.end_time = self.created_at + timedelta(minutes=5)
        super(VerificationCode, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.code}'