from django.contrib import admin
from django.urls import path, include
from tickets.ui_views import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # UI Bootstrap (Django templates)
    path("", include("tickets.urls_ui")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # API REST
    path("api/", include("tickets.urls_api")),
]
