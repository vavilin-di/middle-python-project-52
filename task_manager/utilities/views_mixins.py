__all__ = ["MessageSendingLoginRequiredMixin"]

from collections.abc import Callable
from http import HTTPMethod

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect


class MessageSendingLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для отправки сообщения пользователю при отсутствии прав доступа.

    Расширяет стандартный LoginRequiredMixin, добавляя возможность
    отправки flash-сообщения и перенаправления пользователя на success_url
    возникновении исключения PermissionDenied
    в процессе проверки прав доступа.

    Attributes:
        _no_permissions_message (str): Текст сообщения, отображаемого
            пользователю при отсутствии прав. По умолчанию пустая строка.
        _message_level (int): Уровень сообщения Django messages
            (например, messages.ERROR, messages.SUCCESS). По умолчанию
            messages.ERROR.
    """

    _no_permissions_message = ""
    _message_level = messages.ERROR

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.add_message(self.request, self._message_level, self._no_permissions_message)  # type: ignore
            return redirect(self.success_url)


class MessageSendingUserPassesTestMixin(UserPassesTestMixin):
    """Миксин для отправки сообщения пользователю при невыполнении теста.

    Расширяет стандартный UserPassesTestMixin, добавляя возможность
    отправки flash-сообщения и перенаправления пользователя на success_url при невыполнении теста.
    При обращении по методу GET тест всегда возвращает True для возможности попасть на страницу подтверждения удаления.

    Attributes:
        _test_failure_message (str): Текст сообщения, отображаемого
            пользователю при невыполнении теста. По умолчанию пустая строка.
        _message_level (int): Уровень сообщения Django messages
            (например, messages.ERROR, messages.SUCCESS). По умолчанию
            messages.ERROR.
    """

    _test_failure_message = ""
    _message_level = messages.ERROR

    def get_test_func(self) -> Callable[[], bool]:
        if self.request.method == HTTPMethod.GET:
            return lambda: True
        return super().get_test_func()

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.add_message(self.request, self._message_level, self._test_failure_message)  # type: ignore
            return redirect(self.success_url)
