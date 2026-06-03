"""
Тесты для модуля views_mixins.py.

Модуль task_manager.utilities.views_mixins содержит миксины для представлений:
- MessageSendingLoginRequiredMixin — отправляет flash-сообщение при отсутствии прав
- MessageSendingUserPassesTestMixin — отправляет flash-сообщение при невыполнении теста
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from task_manager.utilities.views_mixins import (
    MessageSendingLoginRequiredMixin,
    MessageSendingUserPassesTestMixin,
)

if TYPE_CHECKING:
    from django.test import RequestFactory


def _setup_request(rf: RequestFactory, method: str = "get") -> object:
    """Создаёт request с middleware и анонимным пользователем."""
    request = getattr(rf, method)("/test/")
    request.user = AnonymousUser()
    SessionMiddleware(lambda req: None).process_request(request)  # type: ignore[arg-type]
    MessageMiddleware(lambda req: None).process_request(request)  # type: ignore[arg-type]
    return request


class TestMessageSendingLoginRequiredMixin:
    """Тесты для MessageSendingLoginRequiredMixin."""

    def test_handle_no_permission_redirects_when_not_authenticated(self, rf: RequestFactory):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        mixin = MessageSendingLoginRequiredMixin()
        mixin.request = _setup_request(rf)  # type: ignore[attr-defined]

        response = mixin.handle_no_permission()
        assert isinstance(response, HttpResponseRedirect)

    def test_handle_no_permission_sends_message_on_permission_denied(self, rf: RequestFactory):
        """При PermissionDenied отправляется flash-сообщение."""
        mixin = MessageSendingLoginRequiredMixin()
        mixin._no_permissions_message = _("Нет прав")
        mixin.success_url = "/test/"  # type: ignore[attr-defined]
        mixin.request = _setup_request(rf)  # type: ignore[attr-defined]

        response = mixin.handle_no_permission()
        assert isinstance(response, HttpResponseRedirect)

    def test_default_message_level_is_error(self):
        """Уровень сообщения по умолчанию — messages.ERROR."""
        mixin = MessageSendingLoginRequiredMixin()
        assert mixin._message_level == messages.ERROR

    def test_default_no_permissions_message_is_empty(self):
        """Сообщение по умолчанию — пустая строка."""
        mixin = MessageSendingLoginRequiredMixin()
        assert mixin._no_permissions_message == ""


class TestMessageSendingUserPassesTestMixin:
    """Тесты для MessageSendingUserPassesTestMixin."""

    def test_get_test_func_returns_true_for_get_request(self, rf: RequestFactory):
        """При GET-запросе test_func всегда возвращает True."""
        mixin = MessageSendingUserPassesTestMixin()
        mixin.request = rf.get("/test/")  # type: ignore[attr-defined]

        test_func = mixin.get_test_func()
        assert test_func() is True

    def test_get_test_func_returns_original_for_post_request(self, rf: RequestFactory):
        """При POST-запросе get_test_func возвращает оригинальный test_func."""
        mixin = _MixinWithTestFunc()
        mixin.request = rf.post("/test/")  # type: ignore[attr-defined]

        test_func = mixin.get_test_func()
        assert test_func() is False

    def test_handle_no_permission_redirects(self, rf: RequestFactory):
        """handle_no_permission возвращает HttpResponseRedirect."""
        mixin = MessageSendingUserPassesTestMixin()
        mixin._test_failure_message = _("Тест не пройден")
        mixin.success_url = "/test/"  # type: ignore[attr-defined]
        mixin.request = _setup_request(rf)  # type: ignore[attr-defined]

        response = mixin.handle_no_permission()
        assert isinstance(response, HttpResponseRedirect)

    def test_default_message_level_is_error(self):
        """Уровень сообщения по умолчанию — messages.ERROR."""
        mixin = MessageSendingUserPassesTestMixin()
        assert mixin._message_level == messages.ERROR

    def test_default_test_failure_message_is_empty(self):
        """Сообщение по умолчанию — пустая строка."""
        mixin = MessageSendingUserPassesTestMixin()
        assert mixin._test_failure_message == ""


class _MixinWithTestFunc(MessageSendingUserPassesTestMixin):
    """Вспомогательный класс с реализацией test_func для тестов."""

    def test_func(self) -> bool:
        return False
