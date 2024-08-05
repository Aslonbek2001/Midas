from rest_framework import viewsets, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, ItemsListSerializer
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from cafe.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied

@extend_schema(
    request=OrderSerializer,
    responses={200: OrderSerializer}
)
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [ 'status', 'order_date']
    search_fields = ['user','order_date', 'total_price']

    def get_queryset(self):
        """
        Foydalanuvchining identifikatorini tekshirishdan avval,
        AnonymousUser holatini hisobga olish.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()  # Agar foydalanuvchi autentifikatsiya qilinmagan bo'lsa
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Yangi buyurtmani yaratuvchi foydalanuvchini belgilash


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Adminlar uchun barcha buyurtmalarni ko'radi, 
        foydalanuvchilar uchun esa faqat o'z buyurtmalarini ko'radi
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)


class OrderItemListView(generics.ListAPIView):
    serializer_class = ItemsListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        order_id = self.kwargs.get('order_id')

        if not order_id:
            raise PermissionDenied("Order ID is required")

        if user.is_staff:
            return OrderItem.objects.filter(order_id=order_id)

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise PermissionDenied("You do not have permission to view these items")

        return OrderItem.objects.filter(order=order)