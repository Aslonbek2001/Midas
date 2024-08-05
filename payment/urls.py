# urls.py
from django.urls import path
from .views import PaymentView, CombinedOrderPaymentView

urlpatterns = [
    # path('api/payment/', PaymentView.as_view(), name='payment'),
    # path('api/check', CombinedOrderPaymentView.as_view(), name='payment'),

]
