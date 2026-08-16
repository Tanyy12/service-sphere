# Instead of manually creating lots of bookings through your website just to test the dashboard, create a command that generates realistic sample bookings for you.
'''
Folder structure will be :
analytics/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── seed_bookings.py
├── models.py
├── views.py
└── ...

The two __init__.py files tells Python/Django that these directories are Python packages 

python manage.py seed_bookings

It's useful when you're building your dashboard and need data to test:

Total bookings
Revenue
Completed bookings
Pending bookings
Cancelled bookings
Services with the most bookings
Provider statistics
Charts and graphs
'''

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
from services.models import Service
from bookings.models import Booking

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed sample bookings for dashboard testing'

    def handle(self, *args, **kwargs):
        customers = User.objects.filter(role='customer')
        services = Service.objects.all()

        if not customers.exists() or not services.exists():
            self.stdout.write(self.style.ERROR('Need at least one customer and one service first.'))
            return

        for i in range(15):
            Booking.objects.create(
                customer=random.choice(customers),
                service=random.choice(services),
                scheduled_at=timezone.now() + timedelta(days=random.randint(1, 10)),
                total_amount=random.choice([30, 50, 75, 100]),
                status=random.choice(['pending', 'confirmed', 'completed']),
                created_at=timezone.now() - timedelta(days=random.randint(0, 14))
            )
        self.stdout.write(self.style.SUCCESS('Seeded 15 sample bookings.'))