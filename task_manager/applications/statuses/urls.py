from __future__ import annotations

__all__ = ["urlpatterns"]

from typing import TYPE_CHECKING

from django.urls import path

from .views import StatusCreateView, StatusDeleteView, StatusListView, StatusUpdateView

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern

urlpatterns: list[URLPattern] = [
    path("create/", StatusCreateView.as_view(), name="create"),
    path("", StatusListView.as_view(), name="list"),
    path("<int:pk>/update/", StatusUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), name="delete"),
]
