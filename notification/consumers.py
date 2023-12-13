import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from websocket.services import JWTService
from urllib.parse import parse_qs

logger = logging.getLogger("django")


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("Connecting to websocket")
        # Parse the query string
        query_string = self.scope["query_string"].decode("utf-8")
        parameters = parse_qs(query_string)

        # Extract the token
        token = parameters.get("token")

        if not token:
            # Handle cases where token is not provided
            # 4000 or any other suitable error code
            await self.close(code=4000)
            return

        token = token[0]

        # Use the service to get the user from the token
        user = await JWTService.get_user_from_token(token)

        # Check if a user was returned, indicating a successful authentication
        if user:
            self.scope["user"] = user
            self.group_name = f"notification_{self.scope['user'].id}"
            # Join the group
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Leave the group when the socket disconnects."""
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This will handle messages sent from the server to the consumer
    async def receive(self, text_data):
        """Receive a message from the socket."""
        pass

    # This will be executed when the server sends a message to the group.
    async def notification_message(self, event):
        """Receive a message from the group."""
        # Send the message to the WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "data": event["data"],
                }
            )
        )
