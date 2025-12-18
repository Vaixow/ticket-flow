import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TicketsLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "tickets_live"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "system",
            "message": "Conectado a TicketFlow Live"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Opcional: permitir ping desde cliente
        if not text_data:
            return
        try:
            data = json.loads(text_data)
        except Exception:
            return

        if data.get("type") == "ping":
            await self.send(text_data=json.dumps({"type": "pong"}))

    async def ticket_event(self, event):
        # event = {"type": "ticket_event", "action": "...", "payload": {...}}
        await self.send(text_data=json.dumps({
            "type": "ticket_event",
            "action": event.get("action"),
            "payload": event.get("payload", {}),
        }))
