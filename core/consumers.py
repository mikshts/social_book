import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message, Comment, Post


# ------------------ CHAT CONSUMER ------------------
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        try:
            receiver_id_int = int(self.receiver_id)
        except ValueError:
            await self.close()
            return

        user_ids = sorted([self.user.id, receiver_id_int])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_content = data.get("message", "").strip()
            message_id = data.get("message_id")

            receiver = await self._get_user(self.receiver_id)
            if not receiver:
                await self.close()
                return

            timestamp = timezone.now()
            await self._save_message(self.user, receiver, message_content, timestamp)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_content,
                    "sender": self.user.username,
                    "sender_id": self.user.id,
                    "timestamp": timestamp.isoformat(),
                    "message_id": message_id,
                }
            )
        except Exception as e:
            print(f"[ChatConsumer Error] {e}")
            await self.close()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "sender_id": event["sender_id"],
            "timestamp": event["timestamp"],
            "message_id": event.get("message_id"),
        }))

    @database_sync_to_async
    def _get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"[ChatConsumer] User with ID {user_id} does not exist.")
            return None

    @database_sync_to_async
    def _save_message(self, sender, receiver, content, timestamp):
        if sender and receiver:
            return Message.objects.create(sender=sender, receiver=receiver, content=content, timestamp=timestamp)


# ------------------ COMMENT CONSUMER ------------------
class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comments_{self.post_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            if not self.scope["user"].is_authenticated:
                await self.close()
                return

            data = json.loads(text_data)
            comment_text = data['text'].strip()
            user_id = self.scope['user'].id

            comment = await self.save_comment(user_id, self.post_id, comment_text)
            profile_img_url = await self.get_profile_img_url(comment.user)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_comment',
                    'username': comment.user.username,
                    'text': comment.text,
                    'profile_img': profile_img_url,
                    'timestamp': comment.timestamp.isoformat(),
                }
            )
        except Exception as e:
            print(f"[CommentConsumer Error] {e}")
            await self.close()

    async def new_comment(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_comment(self, user_id, post_id, text):
        try:
            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)
            return Comment.objects.create(user=user, post=post, text=text)
        except Exception as e:
            print(f"[save_comment Error] {e}")
            return None

    @database_sync_to_async
    def get_profile_img_url(self, user):
        try:
            if hasattr(user, 'profile') and user.profile.profileimg:
                return user.profile.profileimg.url
        except Exception:
            pass
        return '/static/assets/images/default-avatar.jpg'


# ------------------ LIKE CONSUMER ------------------
class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.group_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"[LikeConsumer] Received: {data}")
        except Exception as e:
            print(f"[LikeConsumer Error] {e}")
            await self.close()

    async def send_like_update(self, event):
        await self.send(text_data=json.dumps({
            'post_id': event['post_id'],
            'likes_count': event['likes_count'],
            'recent_likers': event['recent_likers']
        }))


# ------------------ POSTS FEED CONSUMER ------------------
class PostsFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("[PostsFeedConsumer] Connected to 'posts_feed'")
        await self.channel_layer.group_add("posts_feed", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("[PostsFeedConsumer] Disconnected from 'posts_feed'")
        await self.channel_layer.group_discard("posts_feed", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get("action") == "delete_post":
                post_id = int(data.get("post_id", 0))
                await self.channel_layer.group_send(
                    "posts_feed",
                    {
                        "type": "broadcast_post_delete",
                        "post_id": post_id
                    }
                )
        except Exception as e:
            print(f"[PostsFeedConsumer Error] {e}")
            await self.close()

    async def new_post(self, event):
        await self.send(text_data=json.dumps({
            "action": "new_post",
            "html": event["html"]
        }))

    async def broadcast_post_delete(self, event):
        await self.send(text_data=json.dumps({
            "action": "delete_post",
            "post_id": event["post_id"],
            "username": event.get("username", "Unknown"),
        }))
