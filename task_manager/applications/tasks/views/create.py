from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..forms import TaskCreateForm
from ..models import Task


class TaskCreateView(MessageSendingLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("TaskCreatedSuccess")
    _no_permissions_message = _("TaskCreateNoPermission")

    def form_valid(self, form: TaskCreateForm) -> HttpResponse:
        form.instance.author_id = self.request.user.id  # type: ignore
        return super().form_valid(form)
