"""
Тесты для обновления задачи (TaskUpdateView).
"""

from http import HTTPStatus

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


@pytest.mark.django_db
class TestTaskUpdateView:
    """Тесты для обновления задачи."""

    def test_update_task_get_unauthenticated(self, client, create_task):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("tasks:update", kwargs={"pk": create_task.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_update_task_get_authenticated(self, authenticated_client, create_task):
        """GET-запрос возвращает форму редактирования задачи."""
        url = reverse("tasks:update", kwargs={"pk": create_task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "tasks/update.html" for t in response.templates)

    def test_update_task_post_valid(
        self,
        authenticated_client,
        create_task,
        create_second_status,
        create_label,
    ):
        """POST-запрос с валидными данными обновляет задачу и редиректит на список."""
        url = reverse("tasks:update", kwargs={"pk": create_task.pk})
        update_data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "status": create_second_status.pk,
            "executor": create_task.executor.pk,
            "labels": [create_label.pk],
        }
        response = authenticated_client.post(url, data=update_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("tasks:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Задача успешно изменена"))

        create_task.refresh_from_db()
        assert create_task.name == "Updated Task"
        assert create_task.description == "Updated Description"
        assert create_task.status == create_second_status

    def test_update_task_post_invalid(self, authenticated_client, create_task, create_label):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("tasks:update", kwargs={"pk": create_task.pk})
        invalid_data = {
            "name": "",
            "description": "Updated Description",
            "status": create_task.status.pk,
            "executor": create_task.executor.pk,
            "labels": [create_label.pk],
        }
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors
