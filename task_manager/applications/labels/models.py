from django.db import models
from django.utils import timezone


class Label(models.Model):
    class Meta:
        db_table = "labels"
        verbose_name = "Метка"
        verbose_name_plural = "Метки"
        ordering = ["id"]

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Имя", max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(verbose_name="Дата создания", default=timezone.now)

    def __str__(self) -> str:
        return self.name
