from __future__ import annotations

__all__ = ["urlpatterns"]

from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import include, path

from .applications.index.views import CustomLoginView, CustomLogoutView, index
from .applications.labels.urls import urlpatterns as labels_urls
from .applications.statuses.urls import urlpatterns as statuses_urls
from .applications.tasks.urls import urlpatterns as tasks_urls
from .applications.users.urls import urlpatterns as users_urls

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern, URLResolver

urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("login/", CustomLoginView.as_view(redirect_field_name=None), name="login"),
    path("logout/", CustomLogoutView.as_view(redirect_field_name=None), name="logout"),
    path("users/", include((users_urls, "users")), name="users"),
    path("statuses/", include((statuses_urls, "statuses")), name="statuses"),
    path("labels/", include((labels_urls, "labels")), name="labels"),
    path("tasks/", include((tasks_urls, "tasks")), name="tasks"),
    path("i18n/", include("django.conf.urls.i18n")),
]
