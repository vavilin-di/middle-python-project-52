__all__ = ["TaskCreateForm", "TaskUpdateForm"]

from django.forms import ModelForm

from .models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
