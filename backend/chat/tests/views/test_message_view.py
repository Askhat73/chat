from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from chat.models import Room, Message


User = get_user_model()


class MessageViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/v1/messages/"
        user = User.objects.create_user(
            "test",
            email="test@test.com",
            password="secret",
        )
        room = Room.objects.create(name="test1")
        second_room = Room.objects.create(name="test2")
        messages = [
            Message(
                text="1",
                user=user,
                room=room,
                type=Message.Type.MESSAGE,
            ),
            Message(
                text="1",
                user=user,
                room=room,
                type=Message.Type.MESSAGE,
            ),
            Message(
                text="1",
                user=user,
                room=room,
                type=Message.Type.MESSAGE,
            ),
            Message(
                text="2",
                user=user,
                room=second_room,
                type=Message.Type.MESSAGE,
            ),
        ]
        Message.objects.bulk_create(messages)

    def test_url_path(self):
        """Тест url адреса."""
        path = reverse("messages-list")
        self.assertEqual(self.url, path)

    def test_list_messages(self):
        """Тест получения полного списка сообщений."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_room_name(self):
        """Тест фильтрации сообщений."""
        response = self.client.get(self.url, data={"room__name": "test2"})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)
