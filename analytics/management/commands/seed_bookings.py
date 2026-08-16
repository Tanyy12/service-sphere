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