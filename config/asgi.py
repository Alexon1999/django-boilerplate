"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

import websocket.routing  # websocket routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter(
    {
        # "http" for regular HTTP traffic will be handled by Django's urls.py
        "http": get_asgi_application(),
        # Point "websocket" protocol to the routing specified in your_app.routing
        "websocket": URLRouter(websocket.routing.websocket_urlpatterns),
    }
)


# ASGI : (Daphne, Uvicorn, etc.) is asynchronous and
# suitable for handling long-lived connections like WebSockets

# WSGI : (Gunicorn, uWSGI, etc.) is synchronous and
# suitable for handling short-lived requests like HTTP
