from django.db import transaction
from booking.models import Booking
from .serializers import CardInformationSerializer
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.validated_data
            stripe.api_key = settings.STRIPE_SECRET_KEY
            response = self.stripe_card_payment(data_dict=data_dict, request=request)
        else:
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
        return Response(response)

    def stripe_card_payment(self, data_dict, request):
        try:
            # Create a payment method using the test card token
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'token': data_dict['card_token'],  # Use test card token instead of raw card details
                },
            )

            # Modify the payment intent with the payment method id
            payment_intent = stripe.PaymentIntent.create(
                amount=int(request.data['total_price'] * 100),  # Amount should be in cents
                currency='inr',
                payment_method_types=['card'],
            )
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=payment_method['id'],
            )

            try:
                payment_confirm = stripe.PaymentIntent.confirm(payment_intent['id'])
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
            except stripe.error.CardError as e:
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": e.code,
                    "message": e.message,
                    'status': "Failed"
                }

            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                # Update booking status to True
                booking_id = request.data['booking_id']
                booking = Booking.objects.get(pk=booking_id)
                booking.status = True
                booking.save()

                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except stripe.error.InvalidRequestError:
            response = {
                'error': "Invalid request",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        return response
