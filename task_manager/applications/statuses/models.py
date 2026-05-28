__all__ = ["Status"]

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    class Meta:
        db_table = "statuses"
        verbose_name = _("StatusVerboseName")
        verbose_name_plural = _("StatusVerboseNamePlural")
        ordering = ["id"]

    id = models.AutoField(verbose_name=_("StatusID"), primary_key=True)
    name = models.CharField(verbose_name=_("StatusName"), max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(verbose_name=_("StatusCreatedAt"), default=timezone.now)

    def __str__(self) -> str:
        return self.name
