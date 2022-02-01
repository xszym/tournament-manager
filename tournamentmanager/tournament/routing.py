from django.urls import re_path
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/updateScore/(?P<match_slug>.+)/$', consumers.ScoreUpdateConsumer.as_asgi()), # (?P<match_slug>\w+)/$
]
