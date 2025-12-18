from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    creado_por_username = serializers.CharField(source="creado_por.username", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "titulo",
            "descripcion",
            "categoria",
            "prioridad",
            "estado",
            "creado_por",
            "creado_por_username",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["creado_por", "creado_en", "actualizado_en"]
