from __future__ import annotations

__all__ = ["TaskDeleteView"]

from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..models import Task

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase


class TaskDeleteView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, DeleteView):
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
    success_message = _("Задача успешно удалена")

    _no_permissions_message = _("У вас нет прав для удаления задачи")
    _test_failure_message = _("Задачу может удалить только ее автор")

    def _is_author_deleting_task(self) -> bool:
        """
        Проверяет, является ли текущий пользователь автором задачи.

        Returns:
            bool: True, если пользователь — автор задачи, иначе False.
        """

        task_object: Task = self.get_object()
        return task_object.author.id == self.request.user.id  # type: ignore[attr-defined, no-any-return, union-attr]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if not self._is_author_deleting_task():
            messages.add_message(self.request, messages.ERROR, self._test_failure_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
