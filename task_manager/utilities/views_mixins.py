__all__ = ["MessageSendingLoginRequiredMixin"]

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect


class MessageSendingLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для отправки сообщения пользователю при отсутствии прав доступа.

    Расширяет стандартный LoginRequiredMixin, добавляя возможность
    отправки flash-сообщения при возникновении исключения PermissionDenied
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
        """Обрабатывает ситуацию отсутствия прав доступа у пользователя.

        Переопределяет метод родительского класса. Если родительский
        метод выбрасывает исключение PermissionDenied, перехватывает его
        и отправляет пользователю flash-сообщение с заданным уровнем
        и текстом, после чего перенаправляет на success_url.

        Returns:
            HttpResponseRedirect: Перенаправление на success_url
                после отправки сообщения.

        Raises:
            PermissionDenied: Исключение перехватывается внутри метода
                и не пробрасывается наружу.
        """
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.add_message(self.request, self._message_level, self._no_permissions_message)  # type: ignore
            return redirect(self.success_url)
