# serializers.py
from rest_framework import serializers
from .models import Payment
from order.serializers import OrderSerializer
from order.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'


class CombinedOrderPaymentSerializer(serializers.Serializer):
    order = OrderSerializer()
    payment = PaymentSerializer()

    def validate(self, data):
        print("=================CombinedOrderPaymentSerializer == Validate =================")
        return super().validate(data)

    def create(self, validated_data):
        print("=================CombinedOrderPaymentSerializer == Create =================")
        order_data = validated_data.pop('order')
        payment_data = validated_data.pop('payment')

        order = Order.objects.create(**order_data)
        payment_data['order'] = order
        payment = Payment.objects.create(**payment_data)
        
        return {
            'order': order,
            'payment': payment
        }