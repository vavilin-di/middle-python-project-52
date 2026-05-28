__all__ = ["TaskDeleteView"]

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..models import Task


class TaskDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Представление для удаления задачи.

    Требует аутентификации пользователя. Доступ к удалению разрешён
    только автору задачи. При успешном удалении выводится
    всплывающее сообщение об успехе.

    Attributes:
        model (Task): Модель задачи.
        template_name (str): Путь к шаблону подтверждения удаления.
        success_url (str): URL для перенаправления после успешного удаления.
        success_message (str): Сообщение об успешном удалении задачи.
        _no_permissions_message (str): Сообщение при отсутствии прав на удаление.
    """

    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("TaskDeletedSuccess")

    _no_permissions_message = _("TaskDeleteNoPermission")

    def test_func(self) -> bool:
        """
        Проверяет, является ли текущий пользователь автором задачи.

        Returns:
            bool: True, если пользователь — автор задачи, иначе False.
        """

        task_object: Task = self.get_object()
        return task_object.author.id == self.request.user.id  # type: ignore
