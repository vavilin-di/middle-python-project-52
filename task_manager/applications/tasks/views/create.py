__all__ = ["TaskCreateView"]

from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..forms import TaskCreateForm
from ..models import Task


class TaskCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Представление для создания новой задачи.

    Attributes:
        model (Task): Модель задачи.
        form_class (TaskCreateForm): Форма создания задачи.
        template_name (str): Путь к шаблону страницы создания задачи.
        success_url (str): URL для перенаправления после успешного создания.
        success_message (str): Сообщение об успешном создании задачи.
        _no_permissions_message (str): Сообщение при отсутствии прав на создание.
    """

    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("TaskCreatedSuccess")
    _no_permissions_message = _("TaskCreateNoPermission")

    def form_valid(self, form: TaskCreateForm) -> HttpResponse:
        """Устанавливает автора задачи и сохраняет форму.

        Назначает текущего аутентифицированного пользователя автором задачи,
        после чего вызывает стандартную логику сохранения формы.

        Args:
            form (TaskCreateForm): Валидная форма с данными задачи.

        Returns:
            HttpResponse: Ответ с перенаправлением на список задач.
        """
        form.instance.author_id = self.request.user.id  # type: ignore
        return super().form_valid(form)
