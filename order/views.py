from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsStaffOrReadOnly 

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
