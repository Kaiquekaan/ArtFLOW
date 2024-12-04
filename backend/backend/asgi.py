

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.management import call_command
from django.conf import settings

def run_migrations():
    try:
        print("Criando migrações...")
        call_command('makemigrations')  # Cria as migrações com base nos modelos alterados
        
        print("Aplicando migrações...")
        call_command('migrate')  # Aplica as migrações ao banco de dados
        
        print("Migrações criadas e aplicadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar ou aplicar migrações: {e}")

# Certifique-se de que o Django foi configurado corretamente
if settings.configured:
    run_migrations()
else:
    print("Erro: O Django não foi configurado corretamente.")

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

