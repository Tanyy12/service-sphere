"""
ASGI config for servicesphere project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicesphere.settings')

# This MUST be called before importing anything that touches Django models
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,                          # normal Django views/API
    "websocket": JWTAuthMiddleware(                     # WebSocket connections
        URLRouter(websocket_urlpatterns)
    ),
})
