from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestUserUpdateView:
    """Тесты для обновления пользователя."""

    def test_update_user_get_own(self, authenticated_client, create_user):
        """Пользователь может получить форму редактирования своего профиля."""
        url = reverse("users:update", kwargs={"pk": create_user.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert any(t.name == "users/update.html" for t in response.templates)

    def test_update_user_get_other(self, authenticated_client, db):
        """Пользователь не может редактировать чужой профиль - редирект с сообщением об ошибке."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )
        url = reverse("users:update", kwargs={"pk": other_user.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("users:list")

    def test_update_user_post_valid(self, authenticated_client, create_user):
        """POST-запрос с валидными данными обновляет пользователя."""
        url = reverse("users:update", kwargs={"pk": create_user.pk})
        update_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "Name",
            "password1": "NewPassword123",
            "password2": "NewPassword123",
        }
        response = authenticated_client.post(url, data=update_data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("users:list")

        create_user.refresh_from_db()
        assert create_user.username == "updateduser"
        assert create_user.first_name == "Updated"
        assert create_user.last_name == "Name"
        assert create_user.check_password("NewPassword123")

    def test_update_user_post_invalid(self, authenticated_client, create_user):
        """POST-запрос с невалидными данными возвращает форму с ошибками."""
        url = reverse("users:update", kwargs={"pk": create_user.pk})
        invalid_data = {
            "username": "",
            "first_name": "Test",
            "last_name": "User",
            "password1": "short",
            "password2": "mismatch",
        }
        response = authenticated_client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].errors
