# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationCostumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "group_test"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()
        await self.send(text_data=self.user.username)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({'message': self.user.unite.name}))
