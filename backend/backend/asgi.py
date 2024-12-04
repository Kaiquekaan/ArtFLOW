

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.management import call_command

def run_migrations():
    try:
        print("Criando migrações...")
        call_command('makemigrations')  # Cria as migrações com base nos modelos alterados
        
        print("Aplicando migrações...")
        call_command('migrate')  # Aplica as migrações ao banco de dados
        
        print("Migrações criadas e aplicadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar ou aplicar migrações: {e}")

run_migrations()


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

