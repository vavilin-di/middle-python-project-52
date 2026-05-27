from datetime import datetime

from django.db import models


class Label(models.Model):
    class Meta:
        db_table = "labels"
        verbose_name = "Метка"
        verbose_name_plural = "Метки"

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Имя", max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(verbose_name="Дата создания", default=datetime.now)

    def __str__(self) -> str:
        return self.name
