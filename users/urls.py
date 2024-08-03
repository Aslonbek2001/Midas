from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterView, VerifyCodeView, 
    SendVerificationCodeView, ResetPasswordView, 
    ClientProfileUpdateView, ChangePasswordView
    
    )
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify/', VerifyCodeView.as_view(), name='verify'),
    path('api/send-verification/', SendVerificationCodeView.as_view(), name='send-verification'),
    path("api/reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path('api/profile/', ClientProfileUpdateView.as_view(), name='client-profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Token
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]