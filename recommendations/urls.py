from django.urls import path 
from .views import ServiceRecommendationsView

urlpatterns = [
    path('<int:service_id>/', ServiceRecommendationsView.as_view(), name='service-recommendations'),
]