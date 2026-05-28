from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
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
    success_message = _("StatusCreatedSuccess")
    _no_permissions_message = _("StatusCreateNoPermission")


class StatusListView(MessageSendingLoginRequiredMixin, ListView):
    model = Status
    context_object_name = "statuses"
    template_name = "statuses/list.html"
    paginate_by = STATUSES_PER_PAGE

    _no_permissions_message = _("StatusListNoPermission")


class StatusUpdateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusUpdateForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("StatusUpdatedSuccess")

    _no_permissions_message = _("StatusUpdateNoPermission")


class StatusDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("StatusDeletedSuccess")

    _no_permissions_message = _("StatusDeleteNoPermission")

    def test_func(self) -> bool:
        status_object: Status = self.get_object()
        return not status_object.tasks.exists()  # type: ignore
