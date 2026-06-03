from __future__ import annotations

__all__ = ["Task"]

from typing import TYPE_CHECKING

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from task_manager.applications.labels.models import Label
    from task_manager.applications.statuses.models import Status


class Task(models.Model):
    id: models.AutoField = models.AutoField(verbose_name=_("ID"), primary_key=True)
    name: models.CharField = models.CharField(verbose_name=_("Имя"), max_length=255, null=False, unique=True)
    description: models.TextField = models.TextField(verbose_name=_("Описание"), null=False)
    status: models.ForeignKey[Status] = models.ForeignKey(
        verbose_name=_("Статус"),
        to="statuses.Status",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks",
        related_query_name="tasks",
        default=None,
    )
    author: models.ForeignKey[User] = models.ForeignKey(
        verbose_name=_("Автор"),
        to="auth.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks_by_author",
        related_query_name="tasks_by_author",
        default=None,
    )
    executor: models.ForeignKey[User | None] = models.ForeignKey(
        verbose_name=_("Исполнитель"),
        to="auth.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="tasks_by_executor",
        related_query_name="tasks_by_executor",
        default=None,
    )
    labels: models.ManyToManyField[Label, Task] = models.ManyToManyField(
        verbose_name=_("Метки"),
        to="labels.Label",
        related_name="tasks",
        related_query_name="tasks",
        blank=True,
    )
    created_at: models.DateTimeField = models.DateTimeField(verbose_name=_("Дата создания"), default=timezone.now)

    class Meta:
        db_table = "tasks"
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        ordering = ("id",)

    def __str__(self) -> str:
        return str(self.name)
