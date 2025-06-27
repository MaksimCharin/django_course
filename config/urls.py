from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mailing/", include("mailing.urls", namespace="mailing")),
    path("", include("users.urls", namespace="users")),
]
