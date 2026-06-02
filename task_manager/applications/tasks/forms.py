__all__ = ["TaskCreateForm", "TaskUpdateForm"]

from django.contrib.auth.models import User
from django.forms import ModelChoiceField, ModelForm

from task_manager.utilities.annotations import get_user_full_name_annotation

from .models import Task

TASK_CREATE_FIELD_NAMES = ("name", "description", "status", "executor", "labels")
TASK_UPDATE_FIELD_NAMES = ("name", "description", "status", "executor", "labels")


class _UserFullNameModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.full_name


def _get_executor_field() -> _UserFullNameModelChoiceField:
    return _UserFullNameModelChoiceField(
        User.objects.annotate(**get_user_full_name_annotation()),
        required=False,
        label=Task._meta.get_field("executor").verbose_name,  # type: ignore[union-attr]
    )


class TaskCreateForm(ModelForm):
    executor = _get_executor_field()

    class Meta:
        model = Task
        fields = TASK_CREATE_FIELD_NAMES


class TaskUpdateForm(ModelForm):
    executor = _get_executor_field()

    class Meta:
        model = Task
        fields = TASK_UPDATE_FIELD_NAMES
