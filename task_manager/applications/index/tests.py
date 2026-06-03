"""
Тесты для представлений приложения index.

Модуль task_manager.applications.index.views содержит:
- index — главная страница (только GET)
- CustomLoginView — кастомная страница входа
- CustomLogoutView — кастомный выход
- show_logout_message — обработчик сигнала выхода
"""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.test import Client


class TestIndexView:
    """Тесты для главной страницы."""

    def test_index_get_returns_200(self, client: Client):
        """GET-запрос к главной странице возвращает 200."""
        response = client.get(reverse("index"))
        assert response.status_code == HTTPStatus.OK

    def test_index_uses_correct_template(self, client: Client):
        """Главная страница использует шаблон index.html."""
        response = client.get(reverse("index"))
        assert response.status_code == HTTPStatus.OK
        assert "index.html" in [t.name for t in response.templates]

    def test_index_post_returns_405(self, client: Client):
        """POST-запрос к главной странице возвращает 405 (декоратор @require_http_methods)."""
        response = client.post(reverse("index"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestCustomLoginView:
    """Тесты для кастомной страницы входа."""

    def test_login_get_returns_200(self, client: Client):
        """GET-запрос к странице входа возвращает 200."""
        response = client.get(reverse("login"))
        assert response.status_code == HTTPStatus.OK

    def test_login_uses_correct_template(self, client: Client):
        """Страница входа использует шаблон login.html."""
        response = client.get(reverse("login"))
        assert response.status_code == HTTPStatus.OK
        assert "login.html" in [t.name for t in response.templates]

    def test_login_post_valid_redirects_and_shows_message(self, client: Client, create_user, existing_password: str):
        """POST с валидными данными редиректит на главную и показывает сообщение."""
        response = client.post(
            reverse("login"),
            {"username": "existinguser", "password": existing_password},
            follow=True,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("index"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Вы залогинены"))

    def test_login_post_invalid_returns_form(self, client: Client, db):
        """POST с невалидными данными возвращает форму с ошибкой."""
        response = client.post(reverse("login"), {"username": "wrong", "password": "wrong"})
        assert response.status_code == HTTPStatus.OK
        assert "Пожалуйста, введите правильные имя пользователя и пароль" in response.content.decode()


class TestCustomLogoutView:
    """Тесты для кастомного выхода."""

    def test_logout_post_redirects_and_shows_message(self, client: Client, create_user, existing_password: str):
        """POST-запрос на выход редиректит на главную и показывает сообщение."""
        client.login(username="existinguser", password=existing_password)
        response = client.post(reverse("logout"), follow=True)
        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("index"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Вы разлогинены"))
