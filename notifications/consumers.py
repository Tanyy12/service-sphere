import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    # Called the moment the browser opens the WebSocket connection
    async def connect(self):
        self.user = self.scope["user"]  # we'll populate this via middleware in Step 7

        if not self.user.is_authenticated:
            await self.close()  # reject the connection if no valid user
            return

        # Each user gets their own "group" — like a private mailbox
        self.group_name = f"notifications_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()  # confirm the connection is open

    # Called when the browser closes the connection (tab closed, refresh, etc.)
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Called when something elsewhere in the app sends a message to this user's group
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': event['notification_type'],
            'message': event['message'],
        }))