from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestUserDeleteView:
    """Тесты для удаления пользователя."""

    def test_delete_user_get_own(self, authenticated_client, create_user):
        """Пользователь может получить форму удаления своего профиля."""
        url = reverse("users:delete", kwargs={"pk": create_user.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "object" in response.context
        assert any(t.name == "users/delete.html" for t in response.templates)

    def test_delete_user_get_other(self, authenticated_client, db):
        """Пользователь не может удалить чужой профиль - редирект с сообщением об ошибке."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )
        url = reverse("users:delete", kwargs={"pk": other_user.pk})
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("users:list")

    def test_delete_user_post_own(self, authenticated_client, create_user):
        """POST-запрос удаляет пользователя и редиректит на список пользователей."""
        url = reverse("users:delete", kwargs={"pk": create_user.pk})
        response = authenticated_client.post(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("users:list")

        with pytest.raises(User.DoesNotExist):
            User.objects.get(pk=create_user.pk)

    def test_delete_user_post_other(self, authenticated_client, db):
        """Пользователь не может удалить чужой профиль через POST."""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )
        url = reverse("users:delete", kwargs={"pk": other_user.pk})
        response = authenticated_client.post(url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("users:list")

        assert User.objects.filter(pk=other_user.pk).exists()
