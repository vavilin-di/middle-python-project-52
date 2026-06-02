"""
Тесты для CRUD-операций пользователей.
"""

from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


@pytest.mark.django_db
class TestUserCreateView:
    """Тесты для создания пользователя."""

    def test_create_user_get(self, client: Client):
        """GET-запрос возвращает форму создания пользователя."""
        url = reverse("users:create")
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "users/create.html" for t in response.templates)

    def test_create_user_post_valid(self, client: Client, user_data: dict):
        """POST-запрос с валидными данными создает пользователя и редиректит на login."""
        url = reverse("users:create")
        response = client.post(url, data=user_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("login"), HTTPStatus.FOUND)]  # type: ignore

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Пользователь успешно зарегистрирован"))

        user = User.objects.filter(username=user_data["username"]).first()
        assert user is not None
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.check_password(user_data["password1"])

    def test_create_user_post_invalid(self, client: Client):
        """POST-запрос с невалидными данными возвращает форму с ошибками."""
        url = reverse("users:create")
        invalid_data = {
            "username": "",
            "first_name": "Test",
            "last_name": "User",
            "password1": "short",
            "password2": "short",
        }
        response = client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors
