"""
Тесты для списка задач (TaskListView).
"""

from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTaskListView:
    """Тесты для списка задач."""

    def test_list_tasks_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("tasks:list")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_list_tasks_authenticated(self, authenticated_client, create_task):
        """Аутентифицированный пользователь видит список задач."""
        url = reverse("tasks:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "tasks" in response.context
        assert any(t.name == "tasks/list.html" for t in response.templates)

        tasks = response.context["tasks"]
        assert len(tasks) >= 1
        task_dict = tasks[0]
        assert "id" in task_dict
        assert "name" in task_dict
        assert "status_name" in task_dict
        assert "author_name" in task_dict
        assert "executor_name" in task_dict
        assert "created_at" in task_dict

    def test_list_tasks_empty(self, authenticated_client):
        """Список задач пуст, если задачи не созданы."""
        url = reverse("tasks:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "tasks" in response.context
        assert len(response.context["tasks"]) == 0

    def test_list_tasks_filter_by_status(self, authenticated_client, create_task, create_second_status):
        """Фильтрация задач по статусу."""
        url = reverse("tasks:list")
        response = authenticated_client.get(url, data={"status": create_second_status.pk})

        assert response.status_code == HTTPStatus.OK
        assert "tasks" in response.context
        assert len(response.context["tasks"]) == 0

    def test_list_tasks_filter_own_tasks(self, authenticated_client, create_task, create_user, db):
        """Фильтр 'Только свои задачи' показывает только задачи текущего пользователя."""

        url = reverse("tasks:list")
        response = authenticated_client.get(url, data={"own_tasks": "true"})

        assert response.status_code == HTTPStatus.OK
        assert "tasks" in response.context
        for task in response.context["tasks"]:
            assert task["author_name"] == f"{create_user.first_name} {create_user.last_name}"
