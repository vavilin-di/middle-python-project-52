from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.applications.tasks.models import Task


@pytest.mark.django_db
class TestTaskDeleteView:
    """Тесты для удаления задачи."""

    def test_delete_task_get_unauthenticated(self, client, create_task):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("tasks:delete", kwargs={"pk": create_task.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_delete_task_get_authenticated_author(self, authenticated_client, create_task):
        """Автор задачи может получить форму подтверждения удаления."""
        url = reverse("tasks:delete", kwargs={"pk": create_task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "object" in response.context
        assert any(t.name == "tasks/delete.html" for t in response.templates)

    def test_delete_task_get_other_user(self, authenticated_client, create_task, db):
        """Пользователь не может получить форму удаления чужой задачи — редирект."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )
        # Меняем автора задачи на другого пользователя
        create_task.author = other_user
        create_task.save()

        url = reverse("tasks:delete", kwargs={"pk": create_task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("tasks:list")

    def test_delete_task_post_author(self, authenticated_client, create_task):
        """POST-запрос автора удаляет задачу и редиректит на список."""
        url = reverse("tasks:delete", kwargs={"pk": create_task.pk})
        response = authenticated_client.post(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("tasks:list")

        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(pk=create_task.pk)

    def test_delete_task_post_other_user(self, authenticated_client, create_task, db):
        """Пользователь не может удалить чужую задачу через POST."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )
        create_task.author = other_user
        create_task.save()

        url = reverse("tasks:delete", kwargs={"pk": create_task.pk})
        response = authenticated_client.post(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("tasks:list")

        assert Task.objects.filter(pk=create_task.pk).exists()
