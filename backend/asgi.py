# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatroom import routing  # Import your routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Define the WebSocket routing
websocket_application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Add your WebSocket consumer routing here
            routing.websocket_urlpatterns
        )
    ),
})

# Define the overall ASGI application with both HTTP and WebSocket support
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websocket_application,
})
