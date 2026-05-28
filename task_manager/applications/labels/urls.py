__all__ = ["urlpatterns"]

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import LabelCreateView, LabelDeleteView, LabelListView, LabelUpdateView

urlpatterns: list[URLPattern] = [
    path("create/", LabelCreateView.as_view(), name="create"),
    path("", LabelListView.as_view(), name="list"),
    path("<int:pk>/update/", LabelUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", LabelDeleteView.as_view(), name="delete"),
]
