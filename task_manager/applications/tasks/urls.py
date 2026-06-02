from __future__ import annotations

__all__ = ["urlpatterns"]

from typing import TYPE_CHECKING

from django.urls import path

from .views import TaskCreateView, TaskDeleteView, TaskDetailView, TaskListView, TaskUpdateView

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern

urlpatterns: list[URLPattern] = [
    path("create/", TaskCreateView.as_view(), name="create"),
    path("", TaskListView.as_view(), name="list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="delete"),
]
