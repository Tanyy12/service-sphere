from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        instance = Booking(**data)
        instance.clean()
        return data