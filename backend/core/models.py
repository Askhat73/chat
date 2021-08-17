from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardModel(models.Model):
    """Стандартная модель."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата создания"),
    )

    class Meta:
        abstract = True
