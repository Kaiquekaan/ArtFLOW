from django.urls import re_path
from django.urls import path
from .consumers import *

websocket_urlpatterns = [
     re_path(r'ws/online_friends/', OnlineFriendsConsumer.as_asgi()),
     re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]