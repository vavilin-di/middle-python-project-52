__all__ = ["StatusCreateView", "StatusListView", "StatusUpdateView", "StatusDeleteView"]

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin, MessageSendingUserPassesTestMixin

from .forms import StatusCreateForm, StatusUpdateForm
from .models import Status

STATUSES_PER_PAGE = 30
STATUS_LIST_FIELDS = ["id", "name", "created_at"]


class StatusCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Представление для создания нового статуса.

    Требует аутентификации пользователя.
    После успешного создания перенаправляет на список статусов
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Status.
        form_class: Форма создания статуса.
        template_name: Шаблон страницы создания.
        success_url: URL перенаправления после успешного создания.
        success_message: Сообщение об успешном создании статуса.
        _no_permissions_message: Сообщение при отсутствии прав.
    """

    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("StatusCreatedSuccess")
    _no_permissions_message = _("StatusCreateNoPermission")


class StatusListView(MessageSendingLoginRequiredMixin, ListView):
    """Представление для отображения списка статусов.

    Требует аутентификации пользователя.
    Поддерживает постраничную навигацию.

    Attributes:
        model: Модель Status.
        context_object_name: Имя переменной контекста для списка статусов.
        template_name: Шаблон страницы списка.
        paginate_by: Количество статусов на одной странице.
        _no_permissions_message: Сообщение при отсутствии прав.
    """

    model = Status
    context_object_name = "statuses"
    template_name = "statuses/list.html"
    paginate_by = STATUSES_PER_PAGE

    _no_permissions_message = _("StatusListNoPermission")

    def get_queryset(self) -> QuerySet:
        """Возвращает список записей статусов.

        Returns:
            QuerySet: Набор запросов со значениями из списка STATUS_LIST_FIELDS.
        """

        return super().get_queryset().only(*STATUS_LIST_FIELDS)


class StatusUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для редактирования существующего статуса.

    Требует аутентификации пользователя.
    После успешного обновления перенаправляет на список статусов
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Status.
        form_class: Форма обновления статуса.
        template_name: Шаблон страницы редактирования.
        success_url: URL перенаправления после успешного обновления.
        success_message: Сообщение об успешном обновлении статуса.
        _no_permissions_message: Сообщение при отсутствии прав.
    """

    model = Status
    form_class = StatusUpdateForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("StatusUpdatedSuccess")

    _no_permissions_message = _("StatusUpdateNoPermission")


class StatusDeleteView(
    MessageSendingLoginRequiredMixin, MessageSendingUserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """Представление для удаления статуса.

    Требует аутентификации пользователя.
    Перед удалением проверяет, что статус не привязан ни к одной задаче.
    После успешного удаления перенаправляет на список статусов
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Status.
        template_name: Шаблон страницы удаления.
        success_url: URL перенаправления после успешного удаления.
        success_message: Сообщение об успешном удалении статуса.
        _no_permissions_message: Сообщение при отсутствии прав.
    """

    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("StatusDeletedSuccess")

    _no_permissions_message = _("StatusDeleteNoPermission")
    _test_failure_message = _("StatusDeleteLinkedTask")

    def test_func(self) -> bool:
        """Проверяет возможность удаления статуса.

        Статус можно удалить только в том случае, если он не связан ни с одной задачей.
        """

        status_object: Status = self.get_object()
        return not status_object.tasks.exists()  # type: ignore[attr-defined]
