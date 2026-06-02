from http import HTTPStatus

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.applications.labels.models import Label
from task_manager.applications.statuses.models import Status
from task_manager.applications.tasks.models import Task


@pytest.fixture
def label_data() -> dict:
    """Данные для создания метки."""
    return {
        "name": "Test Label",
    }


@pytest.fixture
def create_label(db) -> Label:
    """Создаёт и возвращает метку в базе данных."""
    return Label.objects.create(name="Existing Label")


@pytest.fixture
def create_status(db) -> Status:
    """Создаёт и возвращает статус в базе данных."""
    return Status.objects.create(name="Existing Status")


@pytest.fixture
def create_task_with_label(db, create_status, create_label, create_user) -> Task:
    """Создаёт задачу, привязанную к метке."""
    task = Task.objects.create(
        name="Test Task",
        description="Test Description",
        status=create_status,
        author=create_user,
        executor=create_user,
    )
    task.labels.add(create_label)
    return task


@pytest.mark.django_db
class TestLabelCreateView:
    """Тесты для создания метки."""

    def test_create_label_get_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("labels:create")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_create_label_get_authenticated(self, authenticated_client):
        """GET-запрос возвращает форму создания метки."""
        url = reverse("labels:create")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "labels/create.html" for t in response.templates)

    def test_create_label_post_valid(self, authenticated_client, label_data):
        """POST-запрос с валидными данными создаёт метку и редиректит на список."""
        url = reverse("labels:create")
        response = authenticated_client.post(url, data=label_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("labels:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Метка успешно создана"))

        label = Label.objects.filter(name=label_data["name"]).first()
        assert label is not None
        assert label.name == label_data["name"]

    def test_create_label_post_invalid(self, authenticated_client):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("labels:create")
        invalid_data = {"name": ""}
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors

    def test_create_label_post_duplicate(self, authenticated_client, create_label):
        """POST-запрос с дублирующимся именем возвращает форму с ошибками."""
        url = reverse("labels:create")
        duplicate_data = {"name": create_label.name}
        response = authenticated_client.post(url, data=duplicate_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors


@pytest.mark.django_db
class TestLabelListView:
    """Тесты для списка меток."""

    def test_list_labels_unauthenticated(self, client):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("labels:list")
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_list_labels_authenticated(self, authenticated_client, create_label):
        """Аутентифицированный пользователь видит список меток."""
        url = reverse("labels:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "labels" in response.context
        assert any(t.name == "labels/list.html" for t in response.templates)

        labels = response.context["labels"]
        assert len(labels) >= 1
        label_object = labels[0]
        assert hasattr(label_object, "id")
        assert hasattr(label_object, "name")
        assert hasattr(label_object, "created_at")

    def test_list_labels_empty(self, authenticated_client):
        """Список меток пуст, если метки не созданы."""
        url = reverse("labels:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "labels" in response.context
        assert len(response.context["labels"]) == 0


@pytest.mark.django_db
class TestLabelUpdateView:
    """Тесты для обновления метки."""

    def test_update_label_get_unauthenticated(self, client, create_label):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("labels:update", kwargs={"pk": create_label.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_update_label_get_authenticated(self, authenticated_client, create_label):
        """GET-запрос возвращает форму редактирования метки."""
        url = reverse("labels:update", kwargs={"pk": create_label.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "labels/update.html" for t in response.templates)

    def test_update_label_post_valid(self, authenticated_client, create_label):
        """POST-запрос с валидными данными обновляет метку и редиректит на список."""
        url = reverse("labels:update", kwargs={"pk": create_label.pk})
        update_data = {"name": "Updated Label"}
        response = authenticated_client.post(url, data=update_data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("labels:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Метка успешно изменена"))

        create_label.refresh_from_db()
        assert create_label.name == "Updated Label"

    def test_update_label_post_invalid(self, authenticated_client, create_label):
        """POST-запрос с пустым именем возвращает форму с ошибками."""
        url = reverse("labels:update", kwargs={"pk": create_label.pk})
        invalid_data = {"name": ""}
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors

    def test_update_label_post_duplicate(self, authenticated_client, create_label, db):
        """POST-запрос с именем, которое уже существует, возвращает форму с ошибками."""
        other_label = Label.objects.create(name="Other Label")
        url = reverse("labels:update", kwargs={"pk": create_label.pk})
        duplicate_data = {"name": other_label.name}
        response = authenticated_client.post(url, data=duplicate_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors


@pytest.mark.django_db
class TestLabelDeleteView:
    """Тесты для удаления метки."""

    def test_delete_label_get_unauthenticated(self, client, create_label):
        """Неаутентифицированный пользователь перенаправляется на страницу входа."""
        url = reverse("labels:delete", kwargs={"pk": create_label.pk})
        response = client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("login"))

    def test_delete_label_get_authenticated(self, authenticated_client, create_label):
        """GET-запрос возвращает форму подтверждения удаления метки."""
        url = reverse("labels:delete", kwargs={"pk": create_label.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "object" in response.context
        assert any(t.name == "labels/delete.html" for t in response.templates)

    def test_delete_label_post_success(self, authenticated_client, create_label):
        """POST-запрос удаляет метку без задач и редиректит на список."""
        url = reverse("labels:delete", kwargs={"pk": create_label.pk})
        response = authenticated_client.post(url, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("labels:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Метка успешно удалена"))

        with pytest.raises(Label.DoesNotExist):
            Label.objects.get(pk=create_label.pk)

    def test_delete_label_post_with_task(
        self,
        authenticated_client,
        create_label,
        create_task_with_label,
    ):
        """POST-запрос не удаляет метку, если к ней привязаны задачи."""
        url = reverse("labels:delete", kwargs={"pk": create_label.pk})
        response = authenticated_client.post(url, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert response.redirect_chain == [(reverse("labels:list"), HTTPStatus.FOUND)]

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == str(_("Невозможно удалить метку: существуют связанные задачи"))

        assert Label.objects.filter(pk=create_label.pk).exists()
