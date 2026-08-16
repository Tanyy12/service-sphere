from django.test import TestCase
from django.contrib.auth import get_user_model
from services.models import Service, Category
from .models import Booking

# Create your tests here.

User = get_user_model()

class BookingLogicTests(TestCase):

    def setUp(self):
        self.provider = User.objects.create_user(username='provider1', password='pass123', role='provider')
        self.customer = User.objects.create_user(username='cust1', password='pass123', role='customer')
        self.category = Category.objects.create(name='Cleaning')
        self.service = Service.objects.create(
            provider=self.provider, category=self.category,
            title='House Cleaning', description='Test', price=50
        )

    def test_no_double_booking(self):
        from django.utils import timezone
        slot = timezone.now()
        Booking.objects.create(customer=self.customer, service=self.service, scheduled_at=slot, total_amount=50)
        duplicate = Booking(customer=self.customer, service=self.service, scheduled_at=slot, total_amount=50)
        with self.assertRaises(Exception):
            duplicate.clean()
            duplicate.save()

    def test_invalid_status_transition(self):
        from django.utils import timezone
        booking = Booking.objects.create(
            customer=self.customer, service=self.service,
            scheduled_at=timezone.now(), total_amount=50
        )
        with self.assertRaises(Exception):
            booking.transition_to('completed')
