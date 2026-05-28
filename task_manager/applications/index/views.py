__all__ = ["index", "CustomLoginView", "CustomLogoutView"]

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def index(request: HttpRequest) -> HttpResponse:
    """Рендерит главную страницу приложения.

    Args:
        request (HttpRequest): Входящий HTTP-запрос.

    Returns:
        HttpResponse: Ответ с отрендеренным шаблоном index.html.
    """
    return render(request, "index.html")


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Кастомное представление для входа с сообщением об успехе.

    Наследуется от SuccessMessageMixin и LoginView.
    При успешном входе перенаправляет на главную страницу
    и отображает локализованное сообщение об успешном входе.
    """

    template_name = "login.html"
    success_url = reverse_lazy("index")
    success_message = _("LoginSuccess")


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    """Кастомное представление для выхода с сообщением об успехе.

    Наследуется от SuccessMessageMixin и LogoutView.
    При успешном выходе перенаправляет на главную страницу
    и отображает локализованное сообщение об успешном выходе.
    """

    template_name = None
    success_url = reverse_lazy("index")
    success_message = _("LogoutSuccess")
