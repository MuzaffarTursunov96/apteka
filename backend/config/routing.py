from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from main import consumers

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
                    re_path(
                        r"ws/chat/(?P<chat_box_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()
                    ),
                    re_path(
                        r"ws/messages/(?P<chat_box_name>\w+)/$", consumers.MessageConsumer.as_asgi()
                    ),
                ]

application = ProtocolTypeRouter( 
    {
        "http":get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)