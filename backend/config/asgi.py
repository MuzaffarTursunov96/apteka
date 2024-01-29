
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import re_path
# from main import consumers

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# # URLs that handle the WebSocket connection are placed here.
# from django.conf import settings

# websocket_urlpatterns = [
#     re_path(
#         r"ws/chat/(?P<chat_box_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()
#     ),
#     re_path(
#         r"ws/messages/(?P<chat_box_name>\w+)/$", consumers.MessageConsumer.as_asgi()
#     ),
# ]

# application = ProtocolTypeRouter
# ( 
#     {
#         "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack
#         (
#             URLRouter
#             (
#                 websocket_urlpatterns
#             )
#         ),
#     }
# )

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main.routing import websocket_urlpatterns  # Import your WebSocket URL patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # Add other protocol configurations if needed
})