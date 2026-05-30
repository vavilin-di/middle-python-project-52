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
LABELS_LIST_FIELDS = ["id", "name", "created_at"]


class LabelCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Создание новой метки."""

    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("LabelCreatedSuccess")
    _no_permissions_message = _("LabelCreateNoPermission")


class LabelListView(MessageSendingLoginRequiredMixin, ListView):
    """Список меток с постраничным просмотром (LABELS_PER_PAGE записей на страницу)."""

    model = Label
    context_object_name = "labels"
    template_name = "labels/list.html"
    paginate_by = LABELS_PER_PAGE
    _no_permissions_message = _("LabelListNoPermission")

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
    success_message = _("LabelUpdatedSuccess")
    _no_permissions_message = _("LabelUpdateNoPermission")


class LabelDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Удаление метки.

    Удаление разрешено только если метка не привязана ни к одной задаче.
    """

    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("LabelDeletedSuccess")
    _no_permissions_message = _("LabelDeleteNoPermission")

    def test_func(self):
        """Проверяет, можно ли удалить метку (не должна быть связана с задачами)."""
        label = self.get_object()
        return not label.tasks.exists()
