from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import TaskCreateForm, TaskUpdateForm
from .models import Task


class TaskCreateView(MessageSendingLoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно создана"
    _no_permissions_message = "У вас нет прав для создания задачи"

    def form_valid(self, form: TaskCreateForm) -> Any:
        form.instance.author_id = self.request.user.id  # type: ignore
        return super().form_valid(form)


class TaskListView(MessageSendingLoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    _no_permissions_message = "У вас нет прав для просмотра задач"

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .annotate(
                status_name=F("status__name"),
                author_name=Concat(F("author__first_name"), Value(" "), F("author__last_name")),
                executor_name=Concat(F("executor__first_name"), Value(" "), F("executor__last_name")),
            )
            .values("id", "name", "status_name", "author_name", "executor_name", "created_at")
            .order_by("id")
        )


class TaskDetailView(MessageSendingLoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/detail.html"

    _no_permissions_message = "У вас нет прав для просмотра задачи"

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .annotate(
                status_name=F("status__name"),
                author_name=Concat(F("author__first_name"), Value(" "), F("author__last_name")),
                executor_name=Concat(F("executor__first_name"), Value(" "), F("executor__last_name")),
                label_names=ArrayAgg("labels__name"),
            )
            .values(
                "id", "name", "description", "status_name", "author_name", "executor_name", "label_names", "created_at"
            )
            .order_by("id")
        )


class TaskUpdateView(MessageSendingLoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена"

    _no_permissions_message = "У вас нет прав для обновления задачи"


class TaskDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена"

    _no_permissions_message = "Задачу может удалить только ее автор"

    def test_func(self) -> bool:
        task_object: Task = self.get_object()
        return task_object.author.id == self.request.user.id  # type: ignore
