from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import StatusCreateForm, StatusUpdateForm
from .models import Status

STATUSES_PER_PAGE = 10


class StatusCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
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
    paginate_by = STATUSES_PER_PAGE

    _no_permissions_message = "У вас нет прав для просмотра статусов"


class StatusUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен"

    _no_permissions_message = "У вас нет прав для обновления статуса"


class StatusDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удален"

    _no_permissions_message = "У вас нет прав для удаления статуса"

    def test_func(self) -> bool:
        status_object: Status = self.get_object()
        return not status_object.tasks.exists()  # type: ignore
