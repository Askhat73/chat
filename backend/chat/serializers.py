from django.utils import timezone
from rest_framework import serializers

from chat.enums import MessageType
from chat.models import Room


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
