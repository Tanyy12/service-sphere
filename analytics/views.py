from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from bookings.models import Booking
from services.models import Service

# Create your views here.

class BookingsTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Booking.objects
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(total_bookings=Count('id'))
            .order_by('date')
        )
        return Response(list(data))


class ServicePerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Service.objects
            .annotate(
                booking_count=Count('bookings'),
                total_revenue=Sum('bookings__total_amount')
            )
            .values('title', 'booking_count', 'total_revenue')
            .order_by('-booking_count')
        )
        return Response(list(data))

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')