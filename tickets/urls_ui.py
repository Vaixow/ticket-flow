from django.urls import path
from .ui_views import dashboard, ticket_create, ticket_edit, ticket_delete, export_csv

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("tickets/new/", ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/edit/", ticket_edit, name="ticket_edit"),
    path("tickets/<int:pk>/delete/", ticket_delete, name="ticket_delete"),
    path("dashboard/export.csv", export_csv, name="export_csv"),
]
