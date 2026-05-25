from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import StatusCreateForm, StatusUpdateForm
from .models import Status


class StatusCreateView(MessageSendingLoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно создан"
    _no_permissions_message = "У вас нет прав для создания статуса"


class StatusListView(MessageSendingLoginRequiredMixin, ListView):
    model = Status
    context_object_name = "statuses"
    template_name = "statuses/list.html"

    _no_permissions_message = "У вас нет прав для просмотра статусов"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().values("id", "name", "created_at").order_by("id")


class StatusUpdateView(MessageSendingLoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен"

    _no_permissions_message = "У вас нет прав для обновления статуса"


class StatusDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удален"

    _no_permissions_message = "У вас нет прав для удаления статуса"

    def test_func(self) -> bool:
        status_object: Status = self.get_object()
        return not status_object.tasks.exists()  # type: ignore
