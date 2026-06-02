from http import HTTPStatus

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.applications.statuses.models import Status
from task_manager.applications.tasks.models import Task


@pytest.fixture
def status_data() -> dict:
    """Данные для создания статуса."""
    return {
        "name": "Test Status",
    }


@pytest.fixture
def create_status(db) -> Status:
    """Создаёт и возвращает статус в базе данных."""
    return Status.objects.create(name="Existing Status")


@pytest.fixture
def create_second_status(db) -> Status:
    """Создаёт и возвращает второй статус в базе данных."""
    return Status.objects.create(name="Second Status")


@pytest.fixture
def create_task_with_status(db, create_status, create_user) -> Task:
    """Создаёт задачу, привязанную к статусу."""
    task = Task.objects.create(
        name="Test Task",
        description="Test Description",
        status=create_status,
        author=create_user,
        executor=create_user,
    )
    return task


@pytest.mark.django_db
class TestStatusCreateView:
    """Тесты для создания статуса."""

    def test_create_status_get_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("statuses:create")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_create_status_get_authenticated(self, authenticated_client):
        """GET-запрос возвращает форму создания статуса."""
        url = reverse("statuses:create")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "statuses/create.html" for t in response.templates)

    def test_create_status_post_valid(self, authenticated_client, status_data):
        """POST-запрос с валидными данными создаёт статус и редиректит на список."""
        url = reverse("statuses:create")
        response = authenticated_client.post(url, data=status_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("statuses:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Статус успешно создан"))

        status = Status.objects.filter(name=status_data["name"]).first()
        assert status is not None
        assert status.name == status_data["name"]

    def test_create_status_post_invalid(self, authenticated_client):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("statuses:create")
        invalid_data = {"name": ""}
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors

    def test_create_status_post_duplicate(self, authenticated_client, create_status):
        """POST-запрос с дублирующимся именем возвращает форму с ошибками."""
        url = reverse("statuses:create")
        duplicate_data = {"name": create_status.name}
        response = authenticated_client.post(url, data=duplicate_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors


@pytest.mark.django_db
class TestStatusListView:
    """Тесты для списка статусов."""

    def test_list_statuses_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("statuses:list")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_list_statuses_authenticated(self, authenticated_client, create_status):
        """Аутентифицированный пользователь видит список статусов."""
        url = reverse("statuses:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "statuses" in response.context
        assert any(t.name == "statuses/list.html" for t in response.templates)

        statuses = response.context["statuses"]
        assert len(statuses) >= 1
        status_obj = statuses[0]
        assert status_obj.id is not None
        assert status_obj.name == create_status.name
        assert status_obj.created_at is not None

    def test_list_statuses_empty(self, authenticated_client):
        """Список статусов пуст, если статусы не созданы."""
        url = reverse("statuses:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "statuses" in response.context
        assert len(response.context["statuses"]) == 0


@pytest.mark.django_db
class TestStatusUpdateView:
    """Тесты для обновления статуса."""

    def test_update_status_get_unauthenticated(self, client, create_status):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("statuses:update", kwargs={"pk": create_status.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_update_status_get_authenticated(self, authenticated_client, create_status):
        """GET-запрос возвращает форму редактирования статуса."""
        url = reverse("statuses:update", kwargs={"pk": create_status.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "statuses/update.html" for t in response.templates)

    def test_update_status_post_valid(self, authenticated_client, create_status):
        """POST-запрос с валидными данными обновляет статус и редиректит на список."""
        url = reverse("statuses:update", kwargs={"pk": create_status.pk})
        update_data = {"name": "Updated Status"}
        response = authenticated_client.post(url, data=update_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("statuses:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Статус успешно изменен"))

        create_status.refresh_from_db()
        assert create_status.name == "Updated Status"

    def test_update_status_post_invalid(self, authenticated_client, create_status):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("statuses:update", kwargs={"pk": create_status.pk})
        invalid_data = {"name": ""}
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors

    def test_update_status_post_duplicate(self, authenticated_client, create_status, create_second_status):
        """POST-запрос с именем, которое уже существует, возвращает форму с ошибками."""
        url = reverse("statuses:update", kwargs={"pk": create_status.pk})
        duplicate_data = {"name": create_second_status.name}
        response = authenticated_client.post(url, data=duplicate_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors


@pytest.mark.django_db
class TestStatusDeleteView:
    """Тесты для удаления статуса."""

    def test_delete_status_get_unauthenticated(self, client, create_status):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("statuses:delete", kwargs={"pk": create_status.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_delete_status_get_authenticated(self, authenticated_client, create_status):
        """GET-запрос возвращает форму подтверждения удаления статуса."""
        url = reverse("statuses:delete", kwargs={"pk": create_status.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "object" in response.context
        assert any(t.name == "statuses/delete.html" for t in response.templates)

    def test_delete_status_post_success(self, authenticated_client, create_status):
        """POST-запрос удаляет статус без задач и редиректит на список."""
        url = reverse("statuses:delete", kwargs={"pk": create_status.pk})
        response = authenticated_client.post(url, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("statuses:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Статус успешно удален"))

        with pytest.raises(Status.DoesNotExist):
            Status.objects.get(pk=create_status.pk)

    def test_delete_status_post_with_task(
        self,
        authenticated_client,
        create_status,
        create_task_with_status,
    ):
        """POST-запрос не удаляет статус, если к нему привязаны задачи."""
        url = reverse("statuses:delete", kwargs={"pk": create_status.pk})
        response = authenticated_client.post(url, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("statuses:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Невозможно удалить статус: существуют связанные задачи"))

        assert Status.objects.filter(pk=create_status.pk).exists()
