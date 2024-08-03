# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from .serializers import PaymentSerializer, CombinedOrderPaymentSerializer
from drf_spectacular.utils import extend_schema

class PaymentView(APIView):
    @extend_schema(
        request=PaymentSerializer,
        responses={200: PaymentSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            try:
                charge = stripe.Charge.create(
                    amount=serializer.validated_data['amount'],
                    currency=serializer.validated_data['currency'],
                    description=serializer.validated_data['description'],
                    source=serializer.validated_data['stripe_token']
                )
                return Response({'status': 'success', 'charge_id': charge.id}, status=status.HTTP_200_OK)
            except stripe.error.StripeError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=CombinedOrderPaymentSerializer,
    responses={201: CombinedOrderPaymentSerializer}
)
class CombinedOrderPaymentView(APIView):
    def post(self, request):
        serializer = CombinedOrderPaymentSerializer(data=request.data)
        if serializer.is_valid():
            combined_data = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)