from django.db import models
from django.conf import settings

# Create your models here.

class Notification(models.Model):
    TYPE_CHOICES = (
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('system', 'System'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.user} - {self.message[:30]}"
