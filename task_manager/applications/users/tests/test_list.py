from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserListView:
    """Тесты для списка пользователей."""

    def test_user_list_authenticated(self, authenticated_client, create_user):
        """Аутентифицированный пользователь видит список пользователей."""
        url = reverse("users:list")
        response = authenticated_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "users" in response.context
        assert any(t.name == "users/list.html" for t in response.templates)

        users = response.context["users"]
        assert len(users) >= 1
        user_dict = users[0]
        assert "id" in user_dict
        assert "username" in user_dict
        assert "full_name" in user_dict
        assert "date_joined" in user_dict

    def test_user_list_unauthenticated(self, client):
        """Неаутентифицированный пользователь также видит список пользователей."""
        url = reverse("users:list")
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "users" in response.context
