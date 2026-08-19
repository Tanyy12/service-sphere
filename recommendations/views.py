from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from services.serializers import ServiceSerializer
from .engine import get_recommendations

# Create your views here.

class ServiceRecommendationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_id):
        recommended_services = get_recommendations(service_id)
        serializer = ServiceSerializer(recommended_services, many=True)
        return Response(serializer.data)
