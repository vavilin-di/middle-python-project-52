from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTaskDetailView:
    """Тесты для просмотра задачи."""

    def test_detail_task_unauthenticated(self, client, create_task):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("tasks:detail", kwargs={"pk": create_task.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_detail_task_authenticated(self, authenticated_client, create_task):
        """Аутентифицированный пользователь видит детальную информацию о задаче."""
        url = reverse("tasks:detail", kwargs={"pk": create_task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "task" in response.context
        assert any(t.name == "tasks/detail.html" for t in response.templates)

        task = response.context["task"]
        assert task["id"] == create_task.pk
        assert task["name"] == create_task.name
        assert task["description"] == create_task.description
        assert task["status_name"] == create_task.status.name
        assert task["author_name"] is not None
        assert task["executor_name"] is not None
        assert task["label_names"] == [None]
        assert "created_at" in task

    def test_detail_task_not_found(self, authenticated_client):
        """Запрос несуществующей задачи возвращает 404."""
        url = reverse("tasks:detail", kwargs={"pk": 99999})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.NOT_FOUND
