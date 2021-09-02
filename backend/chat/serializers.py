from django.utils import timezone
from rest_framework import serializers

from chat.enums import MessageType
from chat.models import Room, Message


class MessageSerializer(serializers.Serializer):
    """Сериализатор сообщения."""

    type = serializers.CharField(default=MessageType.MESSAGE.value)
    text = serializers.CharField()
    user_name = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(default=timezone.now())


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name"]


class MessageModelSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username")
    room_name = serializers.CharField(source="room.name")

    class Meta:
        model = Message
        fields = ["id", "text", "user_name", "room_name", "created_at", "type"]
