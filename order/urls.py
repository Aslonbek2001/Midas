from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, OrderItemListView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('order-items/<int:order_id>/', OrderItemListView.as_view(), name='order-item-list'),
]

