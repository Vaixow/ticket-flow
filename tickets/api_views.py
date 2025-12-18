from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Ticket
from .serializers import TicketSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.select_related("creado_por").order_by("-creado_en")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket = serializer.save(creado_por=self.request.user)
        self._broadcast("created", ticket)

    def perform_update(self, serializer):
        ticket = serializer.save()
        self._broadcast("updated", ticket)

    def perform_destroy(self, instance):
        payload = {"id": instance.id, "titulo": instance.titulo}
        instance.delete()
        self._broadcast_payload("deleted", payload)

    def _broadcast(self, action, ticket: Ticket):
        payload = {
            "id": ticket.id,
            "titulo": ticket.titulo,
            "estado": ticket.estado,
            "prioridad": ticket.prioridad,
            "categoria": ticket.categoria,
            "creado_por": ticket.creado_por.username,
            "creado_en": ticket.creado_en.isoformat(),
        }
        self._broadcast_payload(action, payload)

    def _broadcast_payload(self, action, payload: dict):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "tickets_live",
            {
                "type": "ticket_event",
                "action": action,
                "payload": payload,
            },
        )
