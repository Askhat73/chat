import json

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.conf.urls import url
from django.test import TestCase

from chat.consumers import ChatConsumer
from chat.enums import MessageType


class ChatConsumerTests(TestCase):

    USER_NAME = "test_user"
    SECOND_USER_NAME = "test_user2"
    ROOM_NAME = "test"

    def setUp(self):
        settings.CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "channels.layers.InMemoryChannelLayer",
            },
        }
        self.application = ProtocolTypeRouter(
            {
                "websocket": AuthMiddlewareStack(
                    URLRouter(
                        [
                            url(
                                r"ws/chat/(?P<room_name>\w+)/$",
                                ChatConsumer.as_asgi(),
                            ),
                        ]
                    )
                ),
            }
        )

    async def test_success_connect(self):
        """Тест успешного подключения."""
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/chat/{self.ROOM_NAME}/?user_name={self.USER_NAME}",
        )
        connected, _ = await communicator.connect()
        assert connected
        response = await communicator.receive_from()
        data = json.loads(response)
        self.assertEqual(data.get("type"), MessageType.NOTIFICATION.value)
        self.assertEqual(data.get("text"), "вошел(ла) в комнату")
        self.assertEqual(data.get("user_name"), self.USER_NAME)
        await communicator.disconnect()

    async def test_disconnect(self):
        """Тест отключения."""
        communicator_one = WebsocketCommunicator(
            self.application,
            f"/ws/chat/{self.ROOM_NAME}/?user_name={self.USER_NAME}",
        )
        await communicator_one.connect()
        await communicator_one.receive_from()

        communicator_two = WebsocketCommunicator(
            self.application,
            f"/ws/chat/{self.ROOM_NAME}/?user_name={self.SECOND_USER_NAME}",
        )
        await communicator_two.connect()
        await communicator_one.receive_from()
        await communicator_two.disconnect()

        response = await communicator_one.receive_from()
        data = json.loads(response)
        self.assertEqual(data.get("type"), MessageType.NOTIFICATION.value)
        self.assertEqual(data.get("text"), "покинул(а) комнату")
        self.assertEqual(data.get("user_name"), self.SECOND_USER_NAME)
        await communicator_one.disconnect()

    async def test_success_connect_without_username(self):
        """Тест подключения без указания имени пользователя."""
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/chat/{self.ROOM_NAME}/",
        )
        with self.assertRaises(KeyError):
            await communicator.connect()
