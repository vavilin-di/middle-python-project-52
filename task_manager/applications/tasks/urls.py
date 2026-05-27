from django.urls import path
from django.urls.resolvers import URLPattern

from .views import TaskCreateView, TaskDeleteView, TaskDetailView, TaskListView, TaskUpdateView

urlpatterns: list[URLPattern] = [
    path("create/", TaskCreateView.as_view(), name="create"),
    path("", TaskListView.as_view(), name="list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="delete"),
]
