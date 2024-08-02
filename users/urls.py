from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterView, VerifyCodeView, 
    ResendVerificationCodeView, ResendPasswordView, 
    ClientProfileUpdateView
    
    )
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify/', VerifyCodeView.as_view(), name='verify'),
    path('api/resend-verification/', ResendVerificationCodeView.as_view(), name='resend-verification'),
    path("api/reset-password/", ResendPasswordView.as_view(), name="reset-password"),
    path('api/profile/', ClientProfileUpdateView.as_view(), name='client-profile'),
    

    # Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]