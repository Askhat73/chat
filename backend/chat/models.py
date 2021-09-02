from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import StandardModel


class Room(StandardModel):
    """Комната."""

    name = models.CharField(
        max_length=50,
        verbose_name=_("Название комнаты"),
        unique=True,
    )

    class Meta:
        verbose_name = _("Комната")
        verbose_name_plural = _("Комнаты")

    def __str__(self) -> str:
        return self.name


class Message(StandardModel):
    """Сообщение."""

    class Type(models.TextChoices):
        MESSAGE = "chat_message", _("Сообщение")
        NOTIFICATION = "chat_notification", _("Уведомление")

    text = models.TextField(verbose_name=_("Текст сообщения"))
    user = models.ForeignKey(
        "users.CustomUser",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    room = models.ForeignKey(
        "Room",
        related_name="messages",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Комната"),
    )
    type = models.CharField(
        choices=Type.choices,
        max_length=50,
        verbose_name=_("Тип сообщения"),
    )

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")

    def __str__(self) -> str:
        return f"{self.user.username}: {self.text}"
