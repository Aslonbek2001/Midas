from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ClientOrderListAPIView

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-orders/', ClientOrderListAPIView.as_view(), name='client-order-list'),
]
