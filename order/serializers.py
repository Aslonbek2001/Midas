from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import ClientProfileSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id', 
            'user', 
            'quantity', 
            'total_price', 
            'status', 
            'order_date', 
            'order_items',
            'payment_type',
            'payment_status'
            ]
        extra_kwargs = {
            'id': {'read_only': True},
            'payment_status': {'read_only': True},
            }

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order


