import random
from django.core.mail import send_mail
from .models import VerificationCode
from django.core.exceptions import ObjectDoesNotExist
import re

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user):
    code = generate_verification_code()
    try:
        # Foydalanuvchi uchun mavjud bo'lgan verifikatsiya kodini olish
        verfy = VerificationCode.objects.get(user=user)
        # Mavjud bo'lsa, uni o'chirish
        verfy.delete()
    except ObjectDoesNotExist:
        # Agar verifikatsiya kodi mavjud bo'lmasa, hech narsa qilmaymiz
        pass

    # Yangi verifikatsiya kodini yaratish
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
        return True
    else:
        return False
