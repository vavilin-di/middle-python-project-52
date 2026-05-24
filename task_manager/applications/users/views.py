from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
        return super().get_queryset().values("id", "username", "first_name", "last_name", "date_joined").order_by("id")


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен"
    no_permissions_message = "У вас нет прав для изменения"

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.error(self.request, self.no_permissions_message)
            return redirect(self.success_url)

    def test_func(self):
        user = self.get_object()
        return user.id == self.request.user.id


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно удален"
    no_permissions_message = "У вас нет прав для удаления"

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.error(self.request, self.no_permissions_message)
            return redirect(self.success_url)

    def test_func(self):
        user = self.get_object()
        return user.id == self.request.user.id
