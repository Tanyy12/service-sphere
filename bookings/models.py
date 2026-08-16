from django.db import models
from django.conf import settings
from services.models import Service
from django.core.exceptions import ValidationError

# Create your models here.

class Booking(models.Model):
    STATUS_CHOICES = (

        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        overlapping = Booking.objects.filter(
            service = self.service,
            scheduled_at = self.scheduled_at,
            status__in = ['pending', 'confirmed']
        ).exclude(pk = self.pk)
        if overlapping.exists():
            raise ValidationError("This service is already booked at the selected time.")

    VALID_TRANSITIONS = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['completed', 'cancelled'],
        'completed': [],
        'cancelled': [],
    }

    def transition_to(self, new_status):
        if new_status not in self.VALID_TRANSITIONS.get(self.status, []):
            raise ValidationError(f"Cannot move booking from '{self.status}' to '{new_status}'.")
        self.status = new_status
        self.save()

    def __str__(self):
        return f"{self.customer} - {self.service} ({self.status})"

    
