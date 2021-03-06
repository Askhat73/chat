import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.auth import login, logout
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

from .enums import MessageType
from .models import Message, Room
from .serializers import MessageSerializer


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Обрабатывает подключение пользователя по Вебсокету."""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        user_name = parse_qs(self.scope["query_string"].decode("utf8"))["user_name"][0]
        serializer = MessageSerializer(
            data={
                "type": MessageType.NOTIFICATION.value,
                "user_name": user_name,
                "text": "вошел(ла) в комнату",
                "created_at": timezone.now(),
            }
        )
        serializer.is_valid(raise_exception=True)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.set_user(name=user_name)
        await self.channel_layer.group_send(self.room_group_name, serializer.data)
        await self.save_message(serializer.data)
        await self.accept()

    async def disconnect(self, close_code: int):
        """Обрабатывает отключение пользователя от Вебсокета."""
        serializer = MessageSerializer(
            data={
                "type": MessageType.NOTIFICATION.value,
                "user_name": self.user.username,
                "text": "покинул(а) комнату",
                "created_at": timezone.now(),
            }
        )
        serializer.is_valid(raise_exception=True)
        await self.save_message(serializer.data)
        await self.channel_layer.group_send(self.room_group_name, serializer.data)
        await logout(self.scope)
        await database_sync_to_async(self.scope["session"].save)()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str = None, bytes_data: bytes = None):
        """Обрабатывает получение сообщения от Вебсокета."""
        data = json.loads(text_data)
        data["created_at"] = timezone.now()
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.data

        await self.channel_layer.group_send(self.room_group_name, message)
        await self.save_message(message)

    async def chat_message(self, message: dict):
        """Обрабатывает отправку сообщения группам."""
        message["type"] = MessageType.MESSAGE.value
        await self.send(text_data=json.dumps(message))

    async def chat_notification(self, data: dict):
        """Обрабатывает отправку сообщения группам."""
        data["type"] = MessageType.NOTIFICATION.value

        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def set_user(self, name: str) -> None:
        """Авторизует пользователя."""
        self.user, _ = User.objects.get_or_create(username=name)
        async_to_sync(login)(self.scope, self.user)
        self.scope["session"].save()

    @database_sync_to_async
    def save_message(self, message: dict) -> Message:
        """Сохраняет сообщение."""
        message.pop("user_name", None)
        message = Message(**message)
        message.user = self.user
        message.updated_at = message.created_at
        message.room, _ = Room.objects.get_or_create(name=self.room_name)
        return message.save()
