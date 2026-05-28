__all__ = ["TaskListView", "TaskDetailView"]

from typing import Any

from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django_filters import FilterSet
from django_filters.filters import BooleanFilter

from task_manager.utilities.aggregates import ArrayAggregation
from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from ..models import Task

TASKS_PER_PAGE = 10


class TaskListFilter(FilterSet):
    """Набор фильтров для списка задач.

    Позволяет фильтровать задачи по статусу, исполнителю, меткам,
    а также отображать только задачи, созданные текущим пользователем.
    """

    own_tasks = BooleanFilter(
        field_name="author", label=_("TaskFilterOwnTasks"), method="_filter_own_tasks", widget=CheckboxInput
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def _filter_own_tasks(self, queryset: QuerySet, name: str, value: Any) -> QuerySet:
        """Фильтрует queryset, оставляя только задачи текущего пользователя.

        Args:
            queryset: Исходный набор записей задач.
            name: Имя поля фильтра ('author').
            value: Значение фильтра (True/False).

        Returns:
            QuerySet задач, отфильтрованный по автору
        """
        return queryset.filter(author=self.request.user)


class TaskListView(MessageSendingLoginRequiredMixin, ListView):
    """Представление для отображения списка задач с пагинацией и фильтрацией.

    Требует аутентификации пользователя. При отсутствии прав доступа
    отправляет сообщение об ошибке через MessageSendingLoginRequiredMixin.

    Attributes:
        model: Модель Task.
        context_object_name: Имя переменной контекста для списка задач.
        template_name: Путь к шаблону отображения.
        paginate_by: Количество задач на странице.
    """

    model = Task
    context_object_name = "tasks"
    template_name = "tasks/list.html"
    paginate_by = TASKS_PER_PAGE

    _no_permissions_message = _("TaskListNoPermission")

    def get_queryset(self) -> QuerySet:
        """Формирует queryset задач с аннотациями связанных полей.

        Применяет фильтры из TaskListFilter к базовому queryset,
        аннотирует каждую задачу названием статуса, полным именем автора
        и полным именем исполнителя.

        Returns:
            QuerySet задач с полями: id, name, status_name,
            author_name, executor_name, created_at.
        """
        self.filterset = TaskListFilter(self.request.GET, queryset=super().get_queryset(), request=self.request)
        return self.filterset.qs.annotate(
            status_name=F("status__name"),
            author_name=Concat(F("author__first_name"), Value(" "), F("author__last_name")),
            executor_name=Concat(F("executor__first_name"), Value(" "), F("executor__last_name")),
        ).values("id", "name", "status_name", "author_name", "executor_name", "created_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Добавляет форму фильтрации в контекст шаблона.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Словарь контекста с ключом 'filter_form',
            содержащим форму фильтрации.
        """
        context_data = super().get_context_data(**kwargs)
        context_data["filter_form"] = self.filterset.form
        return context_data


class TaskDetailView(MessageSendingLoginRequiredMixin, DetailView):
    """Представление для отображения детальной информации о задаче.

    Требует аутентификации пользователя. При отсутствии прав доступа
    отправляет сообщение об ошибке через MessageSendingLoginRequiredMixin.

    Attributes:
        model: Модель Task.
        context_object_name: Имя переменной контекста для задачи.
        template_name: Путь к шаблону отображения.
    """

    model = Task
    context_object_name = "task"
    template_name = "tasks/detail.html"

    _no_permissions_message = _("TaskDetailNoPermission")

    def get_queryset(self) -> QuerySet:
        """Формирует queryset задачи с аннотациями связанных полей.

        Аннотирует задачу названием статуса, полным именем автора,
        полным именем исполнителя и списком названий меток.

        Returns:
            QuerySet с одной задачей, содержащей поля: id, name,
            description, status_name, author_name, executor_name,
            label_names, created_at.
        """
        return (
            super()
            .get_queryset()
            .annotate(
                status_name=F("status__name"),
                author_name=Concat(F("author__first_name"), Value(" "), F("author__last_name")),
                executor_name=Concat(F("executor__first_name"), Value(" "), F("executor__last_name")),
                label_names=ArrayAggregation("labels__name"),
            )
            .values(
                "id", "name", "description", "status_name", "author_name", "executor_name", "label_names", "created_at"
            )
        )
