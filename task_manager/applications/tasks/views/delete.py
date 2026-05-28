from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..models import Task


class TaskDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена"

    _no_permissions_message = "Задачу может удалить только ее автор"

    def test_func(self) -> bool:
        task_object: Task = self.get_object()
        return task_object.author.id == self.request.user.id  # type: ignore
