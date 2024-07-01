# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
import time
from notification import models
from channels.db import database_sync_to_async


class NotificationCostumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f"notifications_{self.user.username}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name, {
                "type": "notifications.number",
            }
        )

    async def notifications_number(self, event):
        number = event.get('number_of_notifications')

        if number:
            await self.send(text_data=json.dumps({"number_of_notifications": str(number)}))
