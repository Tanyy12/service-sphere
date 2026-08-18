from django.urls import path
from .views import CreatePayPalOrderView, CapturePayPalOrderView

urlpatterns = [
    path('create-order/', CreatePayPalOrderView.as_view(), name='create-order'),
    path('capture-order/', CapturePayPalOrderView.as_view(), name='capture-order'),
]
