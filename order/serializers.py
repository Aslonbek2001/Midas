from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import ClientProfileSerializer

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'product', 'quantity', 'total_price', 'status', 'order_date']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = ClientProfileSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'quantity', 'total_price', 'status', 'order_date', 'order_items']
