from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from chat.models import Room


class RoomViewSetTests(APITestCase):
    def setUp(self):
        self.url = "/api/v1/rooms/"
        Room.objects.bulk_create(
            [
                Room(name="room_1"),
                Room(name="room_2"),
                Room(name="room_3"),
            ]
        )

    def test_url_path(self):
        """Тест url адреса."""
        path = reverse("rooms-list")
        self.assertEqual(self.url, path)

    def test_list_rooms(self):
        """Тест получения полного списка комнат."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_rooms(self):
        """Тест создания комнаты."""
        response = self.client.post(self.url, data={"name": "room_4"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
