from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.forms.widgets import CheckboxInput
from django.views.generic import DetailView, ListView
from django_filters import FilterSet
from django_filters.filters import BooleanFilter
from django_filters.views import FilterView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..models import Task


class TaskListFilter(FilterSet):
    own_tasks = BooleanFilter(
        field_name="author", label="Только свои задачи", method="_filter_own_tasks", widget=CheckboxInput
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def _filter_own_tasks(self, queryset: QuerySet, name: str, value: Any) -> QuerySet:
        return queryset.filter(author=self.request.user)


class TaskListView(MessageSendingLoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    _no_permissions_message = "У вас нет прав для просмотра задач"

    def get_queryset(self) -> QuerySet:
        self.filterset = TaskListFilter(self.request.GET, queryset=super().get_queryset(), request=self.request)
        return self.filterset.qs.annotate(
            status_name=F("status__name"),
            author_name=Concat(F("author__first_name"), Value(" "), F("author__last_name")),
            executor_name=Concat(F("executor__first_name"), Value(" "), F("executor__last_name")),
        ).values("id", "name", "status_name", "author_name", "executor_name", "created_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["filter_form"] = self.filterset.form
        return context_data


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
        )
