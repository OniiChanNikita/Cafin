import asyncio
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction

from .models import MessageChat, MessagerModel
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

from datetime import datetime


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["slug_num"]
        self.group_name = "chat_%s" % self.chat_box_name
        self.message_chat = await sync_to_async(MessageChat.objects.get)(slug_num=self.chat_box_name)

        # self.user = , self.user1
        # if MessageChat.objects.get()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        user_obj = await sync_to_async(User.objects.get)(username=username)
        if message is not None and message != '':
                messager = await sync_to_async(MessagerModel.objects.create)(username=user_obj, message = message)
                await sync_to_async(self.message_chat.user.add)(messager)
                await database_sync_to_async(messager.save)()
                await database_sync_to_async(self.message_chat.save)()
                date_public = await sync_to_async(self.message_chat.user.filter)(username=user_obj)
                date_public = await sync_to_async(date_public.order_by)('created_at')
                date_public = await sync_to_async(date_public.first)()
                await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chatbox_message",
                    "username": username,
                    "message": message,
                    "date_public": str(date_public.created_at) #('%Y.%m.%d %H:%M:%S')
                },
            )

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        date_public = event["date_public"]
        await sync_to_async(print)(username)
        if message is not None and message != '':
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "username": username,
                        "date_public": date_public,
                        # self.message_chat.date_public.strftime("%a %b %d %Y")
                    }
                )
            )

        pass