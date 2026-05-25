from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, QuerySet, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.utilities.views_mixins import MessageSendingLoginRequiredMixin

from .forms import CustomUserCreateForm, CustomUserUpdateForm


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "users/list.html"

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
            .values("id", "username", "full_name", "date_joined")
            .order_by("id")
        )


class UserUpdateView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен"
    _no_permissions_message = "У вас нет прав для изменения"

    def test_func(self) -> bool:
        user: User = self.get_object()
        return user.id == self.request.user.id  # type: ignore


class UserDeleteView(MessageSendingLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно удален"
    _no_permissions_message = "У вас нет прав для удаления"

    def test_func(self) -> bool:
        user: User = self.get_object()
        return user.id == self.request.user.id  # type: ignore
