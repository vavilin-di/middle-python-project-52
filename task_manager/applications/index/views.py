__all__ = ["index", "CustomLoginView", "CustomLogoutView"]

from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.dispatch import receiver
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения"""
    return render(request, "index.html")


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Кастомное представление для входа с сообщением об успехе.

    При успешном входе перенаправляет на главную страницу
    и отображает локализованное сообщение об успешном входе.
    """

    template_name = "login.html"
    success_url = reverse_lazy("index")
    success_message = _("LoginSuccess")


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    """Кастомное представление для выхода с сообщением об успехе.

    При успешном выходе перенаправляет на главную страницу
    и отображает локализованное сообщение об успешном выходе.
    """

    template_name = None
    success_url = reverse_lazy("index")
    success_message = _("LogoutSuccess")


@receiver(user_logged_out)
def show_logout_message(request, **kwargs):
    messages.success(request, _("LogoutSuccess"))
