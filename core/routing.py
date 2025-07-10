# core/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<receiver_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/comments/(?P<post_id>[0-9a-f-]{36})/$', consumers.CommentConsumer.as_asgi()),
    re_path(r'ws/like/(?P<post_id>[0-9a-f-]{36})/$', consumers.LikeConsumer.as_asgi()),
    re_path(r'ws/posts_feed/$', consumers.PostsFeedConsumer.as_asgi()),
]
