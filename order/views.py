from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsStaffOrReadOnly 
from rest_framework import generics

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ClientOrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.orders