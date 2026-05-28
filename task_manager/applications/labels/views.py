from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import LabelCreateForm, LabelUpdateForm
from .models import Label


class LabelCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно создана"
    _no_permissions_message = "У вас нет прав для создания метки"


class LabelListView(MessageSendingLoginRequiredMixin, ListView):
    model = Label
    context_object_name = "labels"
    template_name = "labels/list.html"

    _no_permissions_message = "У вас нет прав для просмотра меток"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().values("id", "name", "created_at")


class LabelUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelUpdateForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно изменена"

    _no_permissions_message = "У вас нет прав для обновления метки"


class LabelDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно удалена"

    _no_permissions_message = "У вас нет прав для удаления метки"

    def test_func(self) -> bool:
        status_object: Label = self.get_object()
        return not status_object.tasks.exists()
