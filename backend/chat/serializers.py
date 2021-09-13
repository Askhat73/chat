from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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

    name = serializers.CharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message=_(
                    "Название комнаты можеть содержать только латинские буквы, цифры "
                    "и нижнее подчеркивание",
                ),
            )
        ],
    )

    class Meta:
        model = Room
        fields = ["id", "name"]


class MessageModelSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username")
    room_name = serializers.CharField(source="room.name")

    class Meta:
        model = Message
        fields = ["id", "text", "user_name", "room_name", "created_at", "type"]
