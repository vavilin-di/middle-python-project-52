__all__ = ["Status"]

from django.db.models import AutoField, CharField, DateTimeField, Model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(Model):
    id: AutoField = AutoField(verbose_name=_("ID"), primary_key=True)
    name: CharField = CharField(verbose_name=_("Имя"), max_length=255, unique=True, null=False)
    created_at: DateTimeField = DateTimeField(verbose_name=_("Дата создания"), default=timezone.now)

    class Meta:
        db_table = "statuses"
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")
        ordering = ("id",)

    def __str__(self) -> str:
        return str(self.name)
