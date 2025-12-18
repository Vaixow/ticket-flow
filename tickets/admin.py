from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "estado", "prioridad", "categoria", "creado_por", "creado_en")
    list_filter = ("estado", "prioridad", "categoria")
    search_fields = ("titulo", "descripcion", "creado_por__username")
