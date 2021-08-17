from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.models import StandardModel


class CustomUser(AbstractUser, StandardModel):
    """Пользователь."""

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
