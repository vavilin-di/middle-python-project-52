from datetime import datetime

from django.db import models


class Task(models.Model):
    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Имя", max_length=255, null=False)
    description = models.TextField(verbose_name="Описание", null=False)
    status = models.ForeignKey(
        verbose_name="Статус",
        to="statuses.Status",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks",
        related_query_name="tasks",
        default=None,
    )
    author = models.ForeignKey(
        verbose_name="Автор",
        to="auth.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks_by_author",
        related_query_name="tasks_by_author",
        default=None,
    )
    executor = models.ForeignKey(
        verbose_name="Исполнитель",
        to="auth.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks_by_executor",
        related_query_name="tasks_by_executor",
        default=None,
    )
    labels = models.ManyToManyField(
        verbose_name="Метки",
        to="labels.Label",
        related_name="tasks",
        related_query_name="tasks",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", default=datetime.now)

    def __str__(self) -> str:
        return self.name
