from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import ClientProfileSerializer
from cafe.models import Product
from cafe.serializers import ProductSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True},
            'id': {'read_only': True},
        }

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        data['price'] = product.get_price() * quantity
        return data

    def create(self, validated_data):
        return super().create(validated_data)


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
            'quantity': {'read_only': True},
            'total_price': {'read_only': True},
            'status': {'read_only': True},
        }

    def validate(self, data):
        order_items = data.get("order_items", [])
        count = 0
        total_price = 0
        for item in order_items:
            count += item['quantity']
            total_price += item['price']
        data['quantity'] = count
        data['total_price'] = total_price
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order



class ProductForItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']


class ItemsListSerializer(serializers.ModelSerializer):
    product = ProductForItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True},
            'id': {'read_only': True},
        }

