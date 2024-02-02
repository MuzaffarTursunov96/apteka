

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
     re_path(
            r"ws/messages/(?P<chat_box_name>\w+)/$", consumers.MessageConsumer.as_asgi()
                    ),
]