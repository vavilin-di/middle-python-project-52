from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")
    success_message = _("LoginSuccess")


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    template_name = None
    success_url = reverse_lazy("index")
    success_message = _("LogoutSuccess")
