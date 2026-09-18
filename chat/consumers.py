import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Room,Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:

        self.room_name =self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user =self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        self.last_message_time = ''

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data: str | None = None) -> None:
        text_data_json =json.load(text_data)
        message = text_data_json['message'].strip()
        if not message:
            return
        room =await self.get_room()
        await self.save_message(room,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type':'chat_message',
            'message':message,
            'username':self.user.username,
            'timestamp':self.last_message_time,
        }
        )
    async def chat_message(self,event):
        message = event['message']
        await self.send(
            text_data=json.dumps(
                {'message':message,
                 'username':event['username'],
                 'timestamp': event['timestamp']}
            )
        )
    async def get_room(self):
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def _get_room():
            room ,created =Room.objects.get_or_create(name=self.room_name)
            return room
        return await _get_room()
    async def save_message(self):
        from channels.db import database_sync_to_async
        @database_sync_to_async
        def _save_message():
            msg =Message.objects.create(user=self.user,room=room,content=message)
            self.last_message_time = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return await _save_message()