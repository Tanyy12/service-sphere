from rest_framework import viewsets, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.utils import send_notification

# Create your views here.

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        booking = self.get_object()
        new_status = request.data.get('status')
        try:
            booking.transition_to(new_status)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        send_notification(
            booking.customer,
            'booking',
            f"Your booking for {booking.service.title} is now {booking.status} !"
        )
        return Response(BookingSerializer(booking).data)

