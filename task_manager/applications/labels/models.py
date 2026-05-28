__all__ = ["Label"]

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    class Meta:
        db_table = "labels"
        verbose_name = _("LabelVerboseName")
        verbose_name_plural = _("LabelVerboseNamePlural")
        ordering = ["id"]

    id = models.AutoField(verbose_name=_("LabelID"), primary_key=True)
    name = models.CharField(verbose_name=_("LabelName"), max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(verbose_name=_("LabelCreatedAt"), default=timezone.now)

    def __str__(self) -> str:
        return self.name
