from __future__ import annotations

__all__ = ["urlpatterns"]

from typing import TYPE_CHECKING

from django.urls import path

from .views import UserCreateView, UserDeleteView, UserListView, UserUpdateView

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern

urlpatterns: list[URLPattern] = [
    path("create/", UserCreateView.as_view(), name="create"),
    path("", UserListView.as_view(), name="list"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
]
