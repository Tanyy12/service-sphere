from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer
from django.conf import settings
from recommendations.engine import get_recommendations

# Create your views here.

# DRF API VIEWS

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


# TEMPLATE RENDERED PAGES

def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {
        'service': service,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
        })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    recommended = get_recommendations(service.pk)
    return render(request, 'services/service_detail.html', {
        'service': service,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        'recommended_services': recommended
    })