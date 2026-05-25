from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect


class MessageSendingLoginRequiredMixin(LoginRequiredMixin):
    _no_permissions_message = ""
    _message_level = messages.ERROR

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            messages.add_message(self.request, self._message_level, self._no_permissions_message)  # type: ignore
            return redirect(self.success_url)
