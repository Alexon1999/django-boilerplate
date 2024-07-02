# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
import json


class NotificationCostumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f"notifications_{self.user.username}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.group_name, {
                "type": "init",
            }
        )

    async def init(self, event):
        number = await database_sync_to_async(self.user.notifications.unread().count)()
        await self.send(text_data=json.dumps({"number_of_notifications": str(number)}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        await self.channel_layer.group_send(
            self.group_name, {
                "type": "notifications.number",
            }
        )

    async def notifications_number(self, event):
        number = event.get('number_of_notifications')

        if number:
            await self.send(text_data=json.dumps({"number_of_notifications": str(number)}))
