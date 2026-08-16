from django.urls import path
from .views import BookingsTrendView, ServicePerformanceView, dashboard_view

urlpatterns = [
    path('bookings-trend/', BookingsTrendView.as_view(), name='bookings-trend'),
    path('service-performance/', ServicePerformanceView.as_view(), name='service-performance'),
    path('dashboard-page/', dashboard_view, name='dashboard-page'),
]