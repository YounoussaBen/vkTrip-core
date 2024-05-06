from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from booking.models import Booking

class PaymentAPI(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY

                # Create a payment method using the card token
                payment_method = stripe.PaymentMethod.create(
                    type='card',
                    card={
                        'token': data['card_token'],
                    },
                )

                # Create a payment intent
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(data['total_price'] * 100),
                    currency='inr',
                    payment_method_types=['card'],
                    payment_method=payment_method['id'],
                    confirm=True,
                )

                # Handle payment confirmation
                if payment_intent['status'] == 'succeeded':
                    # Update booking status to True
                    booking_id = str(data['booking_id'])
                    booking = Booking.objects.get(pk=booking_id)
                    booking.status = True
                    booking.save()

                    # Save payment record
                    payment = Payment.objects.create(
                        booking_id=booking,
                        user=request.user,  # Assuming user is authenticated
                        total_price=data['total_price'],
                        payment_status=Payment.SUCCESS,
                        payment_intent_id=payment_intent['id'],
                        payment_method_id=payment_method['id'],
                        card_token=data['card_token'],
                    )

                    response_data = {
                        'message': "Card Payment Success",
                        'status': status.HTTP_200_OK,
                        "payment": PaymentSerializer(payment).data
                    }
                    return Response(response_data)
                else:
                    response_data = {
                        'message': "Card Payment Failed",
                        'status': status.HTTP_400_BAD_REQUEST,
                        "payment_intent": payment_intent,
                    }
                    return Response(response_data)
            except stripe.error.StripeError as e:
                response_data = {
                    'error': "Stripe error: " + str(e),
                    'status': status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data)
        else:
            return Response({'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
