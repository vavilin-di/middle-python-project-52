__all__ = ["urlpatterns"]

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import StatusCreateView, StatusDeleteView, StatusListView, StatusUpdateView

urlpatterns: list[URLPattern] = [
    path("create/", StatusCreateView.as_view(), name="create"),
    path("", StatusListView.as_view(), name="list"),
    path("<int:pk>/update/", StatusUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), name="delete"),
]
