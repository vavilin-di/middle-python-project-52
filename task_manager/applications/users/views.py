__all__ = ["UserCreateView", "UserListView", "UserUpdateView", "UserDeleteView"]

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import CustomUserCreateForm, CustomUserUpdateForm

USERS_PER_PAGE = 10


class UserCreateView(SuccessMessageMixin, CreateView):
    """Представление для регистрации нового пользователя.

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


class UserUpdateView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
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

    def test_func(self) -> bool:
        """Проверяет, что текущий пользователь редактирует свой собственный профиль.

        Returns:
            bool: True, если ID пользователя из URL совпадает с ID текущего
                  авторизованного пользователя, иначе False.
        """
        user: User = self.get_object()
        return user.id == self.request.user.id  # type: ignore


class UserDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
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

    def test_func(self) -> bool:
        """Проверяет, что текущий пользователь удаляет свой собственный профиль.

        Returns:
            bool: True, если ID пользователя из URL совпадает с ID текущего
                  авторизованного пользователя, иначе False.
        """
        user: User = self.get_object()
        return user.id == self.request.user.id  # type: ignore
