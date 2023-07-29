import os, django
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebapp.settings')  # Replace 'myproject' with your project name
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from myapp import consumers



# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
    re_path(
        r"chat/(?P<slug_num>\d+)/$", consumers.ChatRoomConsumer.as_asgi()
    ),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)

