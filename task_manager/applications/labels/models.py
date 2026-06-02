__all__ = ["Label"]

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    id = models.AutoField(verbose_name=_("ID"), primary_key=True)
    name = models.CharField(verbose_name=_("Имя"), max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(verbose_name=_("Дата создания"), default=timezone.now)

    class Meta:
        db_table = "labels"
        verbose_name = _("Метка")
        verbose_name_plural = _("Метки")
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name
