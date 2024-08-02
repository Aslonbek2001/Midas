import random
from django.core.mail import send_mail
from .models import VerificationCode

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user):
    code = generate_verification_code()
    VerificationCode.objects.create(user=user, code=code)
    send_mail(
        'Your Verification Code',
        f'Your verification code is {code}',
        'firmaalar@example.com',
        [user.email],
        fail_silently=False,
    )