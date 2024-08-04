import random
from django.core.mail import send_mail
from .models import VerificationCode
import re

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user):
    code = generate_verification_code()
    verfy = VerificationCode.objects.get(user=user)
    verfy.delete()
    VerificationCode.objects.create(user=user, code=code)
    send_mail(
        'Your Verification Code',
        f'Your verification code is {code}',
        'firmaalar@example.com',
        [user.email],
        fail_silently=False,
    )


def check_phone(phone):
    uz_phone_regex = r'^\+998\d{9}$'
    if re.match(uz_phone_regex, phone):
        return False
    else:
        return True
