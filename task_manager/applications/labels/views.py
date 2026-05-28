__all__ = ["LabelCreateView", "LabelListView", "LabelUpdateView", "LabelDeleteView"]

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import LabelCreateForm, LabelUpdateForm
from .models import Label

LABELS_PER_PAGE = 10


class LabelCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Представление для создания новой метки.

    Требует аутентификации пользователя.
    После успешного создания перенаправляет на список меток
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Label.
        form_class: Форма создания метки LabelCreateForm.
        template_name: Шаблон для отображения формы.
        success_url: URL для перенаправления после успешного создания.
        success_message: Сообщение об успешном создании метки.
        _no_permissions_message: Сообщение при отсутствии прав доступа.
    """

    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("LabelCreatedSuccess")
    _no_permissions_message = _("LabelCreateNoPermission")


class LabelListView(MessageSendingLoginRequiredMixin, ListView):
    """Представление для отображения списка меток.

    Требует аутентификации пользователя.
    Поддерживает пагинацию (LABELS_PER_PAGE записей на страницу).

    Attributes:
        model: Модель Label.
        context_object_name: Имя переменной контекста для шаблона.
        template_name: Шаблон для отображения списка.
        paginate_by: Количество меток на странице.
        _no_permissions_message: Сообщение при отсутствии прав доступа.
    """

    model = Label
    context_object_name = "labels"
    template_name = "labels/list.html"
    paginate_by = LABELS_PER_PAGE

    _no_permissions_message = _("LabelListNoPermission")

    def get_queryset(self) -> QuerySet:
        """Возвращает набор запросов для списка меток.

        Ограничивает выборку полями id, name и created_at
        для оптимизации загрузки данных.

        Returns:
            QuerySet: Набор запросов со значениями id, name, created_at.
        """
        return super().get_queryset().values("id", "name", "created_at")


class LabelUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для редактирования существующей метки.

    Требует аутентификации пользователя.
    После успешного обновления перенаправляет на список меток
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Label.
        form_class: Форма обновления метки LabelUpdateForm.
        template_name: Шаблон для отображения формы.
        success_url: URL для перенаправления после успешного обновления.
        success_message: Сообщение об успешном обновлении метки.
        _no_permissions_message: Сообщение при отсутствии прав доступа.
    """

    model = Label
    form_class = LabelUpdateForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("LabelUpdatedSuccess")

    _no_permissions_message = _("LabelUpdateNoPermission")


class LabelDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Представление для удаления метки.

    Требует аутентификации пользователя.
    Удаление разрешено только если метка не привязана ни к одной задаче.
    После успешного удаления перенаправляет на список меток
    и выводит сообщение об успехе.

    Attributes:
        model: Модель Label.
        template_name: Шаблон для отображения подтверждения удаления.
        success_url: URL для перенаправления после успешного удаления.
        success_message: Сообщение об успешном удалении метки.
        _no_permissions_message: Сообщение при отсутствии прав доступа.
    """

    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("LabelDeletedSuccess")

    _no_permissions_message = _("LabelDeleteNoPermission")

    def test_func(self) -> bool:
        """Проверяет, можно ли удалить метку.

        Метка может быть удалена только в том случае,
        если она не связана ни с одной задачей.

        Returns:
            bool: True, если метку можно удалить (нет связанных задач),
                  иначе False.
        """
        status_object: Label = self.get_object()
        return not status_object.tasks.exists()  # type: ignore
