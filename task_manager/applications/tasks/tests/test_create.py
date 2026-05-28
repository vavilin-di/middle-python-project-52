from http import HTTPStatus

import pytest
from django.urls import reverse

from task_manager.applications.tasks.models import Task


@pytest.mark.django_db
class TestTaskCreateView:
    """Тесты для создания задачи."""

    def test_create_task_get_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("tasks:create")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_create_task_get_authenticated(self, authenticated_client):
        """GET-запрос возвращает форму создания задачи."""
        url = reverse("tasks:create")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "tasks/create.html" for t in response.templates)

    def test_create_task_post_valid(
        self,
        authenticated_client,
        create_user,
        create_status,
        create_label,
    ):
        """POST-запрос с валидными данными создаёт задачу и редиректит на список."""
        url = reverse("tasks:create")
        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": create_status.pk,
            "executor": create_user.pk,
            "labels": [create_label.pk],
        }
        response = authenticated_client.post(url, data=task_data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("tasks:list")

        task = Task.objects.filter(name=task_data["name"]).first()
        assert task is not None
        assert task.name == task_data["name"]
        assert task.description == task_data["description"]
        assert task.status == create_status
        assert task.executor == create_user
        assert task.author == create_user
        assert list(task.labels.values_list("id", flat=True)) == [create_label.pk]

    def test_create_task_post_invalid(self, authenticated_client):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("tasks:create")
        invalid_data = {
            "name": "",
            "description": "Test Description",
        }
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors
