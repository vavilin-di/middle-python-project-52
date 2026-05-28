from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..forms import TaskUpdateForm
from ..models import Task


class TaskUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена"

    _no_permissions_message = "У вас нет прав для обновления задачи"
