__all__ = ["UserCreateView", "UserListView", "UserUpdateView", "UserDeleteView"]

from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import CustomUserCreateForm, CustomUserUpdateForm

USERS_PER_PAGE = 10


class _OwnProfilePermissionMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь работает со своим профилем.

    Устраняет дублирование test_func() между UserUpdateView и UserDeleteView.
    Рассчитан на использование вместе с SingleObjectMixin (UpdateView, DeleteView).
    """

    def test_func(self) -> bool:
        """Проверяет, что ID пользователя из URL совпадает с ID текущего пользователя.

        Returns:
            True, если пользователь редактирует/удаляет свой профиль, иначе False.
        """
        user: User = self.get_object()  # type: ignore[attr-defined]
        return user.pk == self.request.user.pk  # type: ignore[attr-defined]


class UserCreateView(SuccessMessageMixin, CreateView):
    """Представление для регистрации нового пользователя.

    Не требует аутентификации — это точка входа в приложение.
    При успешной регистрации перенаправляет на страницу входа
    и выводит всплывающее сообщение об успехе.
    """

    model = User
    form_class = CustomUserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("UserCreatedSuccess")


class UserListView(ListView):
    """Представление для отображения списка пользователей.

    Доступно без аутентификации (см. тест test_user_list_unauthenticated).
    Поддерживает пагинацию (USERS_PER_PAGE записей на страницу).
    В queryset добавляется вычисляемое поле full_name,
    сформированное из first_name и last_name через пробел.
    """

    model = User
    context_object_name = "users"
    template_name = "users/list.html"
    paginate_by = USERS_PER_PAGE

    def get_queryset(self) -> QuerySet:
        """Возвращает список пользователей с аннотированным полем full_name.

        Returns:
            QuerySet: набор записей с полями id, username, full_name, date_joined,
                      отсортированный по id.
        """
        return (
            super()
            .get_queryset()
            .annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
            .values("id", "username", "full_name", "date_joined")
            .order_by("id")
        )


class UserUpdateView(MessageSendingLoginRequiredMixin, _OwnProfilePermissionMixin, SuccessMessageMixin, UpdateView):
    """Представление для редактирования профиля пользователя.

    Доступно только авторизованному пользователю для его собственной учётной записи.
    При успешном обновлении перенаправляет на список пользователей
    и выводит всплывающее сообщение об успехе.
    """

    model = User
    form_class = CustomUserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    success_message = _("UserUpdatedSuccess")
    _no_permissions_message = _("UserUpdateNoPermission")


class UserDeleteView(MessageSendingLoginRequiredMixin, _OwnProfilePermissionMixin, SuccessMessageMixin, DeleteView):
    """Представление для удаления учётной записи пользователя.

    Доступно только авторизованному пользователю для его собственной учётной записи.
    При успешном удалении перенаправляет на список пользователей
    и выводит всплывающее сообщение об успехе.
    """

    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("UserDeletedSuccess")
    _no_permissions_message = _("UserDeleteNoPermission")

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Завершает сессию перед удалением пользователя.

        Если пользователь удаляет сам себя, необходимо вызвать logout(),
        иначе после удаления записи из БД сессия останется активной,
        что приведёт к ошибкам при последующих запросах.
        """
        logout(request)
        return super().post(request, *args, **kwargs)
