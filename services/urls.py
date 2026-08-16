from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ServiceViewSet, service_detail, service_list

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('services', ServiceViewSet)

urlpatterns = router.urls + [
    path('services-page/', service_list, name='service-list'),
    path('services-page/<int:pk>/', service_detail, name='service-detail'),
]