from __future__ import annotations

__all__ = ["urlpatterns"]

from typing import TYPE_CHECKING

from django.urls import path

from .views import LabelCreateView, LabelDeleteView, LabelListView, LabelUpdateView

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern

urlpatterns: list[URLPattern] = [
    path("create/", LabelCreateView.as_view(), name="create"),
    path("", LabelListView.as_view(), name="list"),
    path("<int:pk>/update/", LabelUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", LabelDeleteView.as_view(), name="delete"),
]
