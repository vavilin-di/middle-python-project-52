__all__ = ["TaskUpdateView"]

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..forms import TaskUpdateForm
from ..models import Task


class TaskUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления существующей задачи.

    Attributes:
        model (Type[Task]): Модель задачи.
        form_class (Type[TaskUpdateForm]): Форма обновления задачи.
        template_name (str): Путь к шаблону страницы обновления.
        success_url (str): URL перенаправления после успешного обновления.
        success_message (str): Сообщение об успешном обновлении задачи.
        _no_permissions_message (str): Сообщение об отсутствии прав на обновление.
    """

    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("TaskUpdatedSuccess")

    _no_permissions_message = _("TaskUpdateNoPermission")
