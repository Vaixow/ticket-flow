from django.urls import re_path
from .consumers import TicketsLiveConsumer

websocket_urlpatterns = [
    re_path(r"ws/tickets/$", TicketsLiveConsumer.as_asgi()),
]
