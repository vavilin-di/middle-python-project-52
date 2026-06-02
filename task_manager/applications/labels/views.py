__all__ = ["LabelCreateView", "LabelListView", "LabelUpdateView", "LabelDeleteView"]

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin, MessageSendingUserPassesTestMixin

from .forms import LabelCreateForm, LabelUpdateForm
from .models import Label

LABELS_PER_PAGE = 30
LABELS_LIST_FIELDS = ["id", "name", "created_at"]


class LabelCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Создание новой метки."""

    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Метка успешно создана")
    _no_permissions_message = _("У вас нет прав для создания метки")


class LabelListView(MessageSendingLoginRequiredMixin, ListView):
    """Список меток с постраничным просмотром (LABELS_PER_PAGE записей на страницу)."""

    model = Label
    context_object_name = "labels"
    template_name = "labels/list.html"
    paginate_by = LABELS_PER_PAGE
    _no_permissions_message = _("У вас нет прав для просмотра меток")

    def get_queryset(self) -> QuerySet:
        """Возвращает список записей меток.
        Returns:
            QuerySet: Набор запросов со значениями из списка LABELS_LIST_FIELDS."""

        return super().get_queryset().only(*LABELS_LIST_FIELDS)


class LabelUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Редактирование существующей метки."""

    model = Label
    form_class = LabelUpdateForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Метка успешно изменена")
    _no_permissions_message = _("У вас нет прав для обновления метки")


class LabelDeleteView(
    MessageSendingLoginRequiredMixin, MessageSendingUserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """Проверяет возможность удаления метки.

    Метку можно удалить только в том случае, если она не связана ни с одной задачей.
    """

    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Метка успешно удалена")
    _no_permissions_message = _("У вас нет прав для удаления метки")
    _test_failure_message = _("Невозможно удалить метку: существуют связанные задачи")

    def test_func(self) -> bool:
        """Проверяет, можно ли удалить метку (не должна быть связана с задачами)."""
        label = self.get_object()
        return not label.tasks.exists()
