from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from bookings.models import Booking
from .models import Payment
from .paypal_client import get_paypal_client
from notifications.utils import send_notification
from django.utils import timezone

# Create your views here.

class CreatePayPalOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = Booking.objects.get(id=booking_id, customer=request.user)

        client = get_paypal_client()
        req = OrdersCreateRequest()
        req.prefer('return=representation')
        req.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": str(booking.total_amount)
                }
            }]
        })

        response = client.execute(req)
        order_id = response.result.id

        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                'paypal_order_id': order_id,
                'amount': booking.total_amount,
                'status': 'created'
            }
        )

        return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)

class CapturePayPalOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')

        client = get_paypal_client()
        req = OrdersCaptureRequest(order_id)
        response = client.execute(req)

        payment = Payment.objects.get(paypal_order_id=order_id)

        if response.result.status == 'COMPLETED':
            payment.status = 'captured'
            payment.paid_at = timezone.now()
            payment.save()

            payment.booking.transition_to('confirmed')

            send_notification(
                payment.booking.customer,
                'payment',
                f"Payment for {payment.booking.service.title} was successful."
            )

            return Response({'status': 'success'})
        else:
            payment.status = 'failed'
            payment.save()
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)