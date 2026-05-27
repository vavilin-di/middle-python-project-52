"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver

from .applications.index.views import CustomLoginView, CustomLogoutView, index
from .applications.labels.urls import urlpatterns as labels_urls
from .applications.statuses.urls import urlpatterns as statuses_urls
from .applications.tasks.urls import urlpatterns as tasks_urls
from .applications.users.urls import urlpatterns as users_urls

urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("login/", CustomLoginView.as_view(redirect_field_name=None), name="login"),
    path("logout/", CustomLogoutView.as_view(redirect_field_name=None), name="logout"),
    path("users/", include((users_urls, "users")), name="users"),
    path("statuses/", include((statuses_urls, "statuses")), name="statuses"),
    path("labels/", include((labels_urls, "labels")), name="labels"),
    path("tasks/", include((tasks_urls, "tasks")), name="tasks"),
]
