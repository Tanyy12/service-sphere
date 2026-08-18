from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from django.conf import settings


def get_paypal_client():
    environment = SandboxEnvironment(
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    return PayPalHttpClient(environment)