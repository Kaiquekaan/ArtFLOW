

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Aplicação ASGI
application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            __import__('api.routing').routing.websocket_urlpatterns
        )
    ),
})

