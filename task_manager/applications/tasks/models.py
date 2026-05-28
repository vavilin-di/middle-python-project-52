from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class Meta:
        db_table = "tasks"
        verbose_name = _("TaskVerboseName")
        verbose_name_plural = _("TaskVerboseNamePlural")
        ordering = ["id"]

    id = models.AutoField(verbose_name=_("TaskID"), primary_key=True)
    name = models.CharField(verbose_name=_("TaskName"), max_length=255, null=False)
    description = models.TextField(verbose_name=_("TaskDescription"), null=False)
    status = models.ForeignKey(
        verbose_name=_("Status"),
        to="statuses.Status",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks",
        related_query_name="tasks",
        default=None,
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        to="auth.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks_by_author",
        related_query_name="tasks_by_author",
        default=None,
    )
    executor = models.ForeignKey(
        verbose_name=_("Executor"),
        to="auth.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="tasks_by_executor",
        related_query_name="tasks_by_executor",
        default=None,
    )
    labels = models.ManyToManyField(
        verbose_name=_("Labels"),
        to="labels.Label",
        related_name="tasks",
        related_query_name="tasks",
    )
    created_at = models.DateTimeField(verbose_name=_("TaskCreatedAt"), default=timezone.now)

    def __str__(self) -> str:
        return self.name
