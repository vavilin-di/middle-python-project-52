__all__ = ["urlpatterns"]

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import UserCreateView, UserDeleteView, UserListView, UserUpdateView

urlpatterns: list[URLPattern] = [
    path("create/", UserCreateView.as_view(), name="create"),
    path("", UserListView.as_view(), name="list"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
]
