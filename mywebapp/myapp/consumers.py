import asyncio
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction

from .models import MessageChat
from asgiref.sync import sync_to_async

from datetime import datetime


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["slug_num"]
        self.group_name = "chat_%s" % self.chat_box_name
        self.message_chat = await sync_to_async(MessageChat.objects.get)(slug_num=self.chat_box_name)

        #if self.message_chat.message is not None:
        #    for messages in self.message_chat.message:
        #        message_dict = {messages['username']: messages['message']}
        #        for username, message in message_dict.items():
        #           if
        #               await self.channel_layer.group_send(
        #                    self.group_name,
        #                    {
        #                        "type": "chatbox_message",
        #                       "username": username,
        #                        "message": message,
        #
        #                    }
        #                )

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
        # await MessageChat.objects.create
        if message is not None and message != '':
                await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chatbox_message",
                    "username": username,
                    "message": message,
                    "date_public": str(self.message_chat.date_public.strftime("%a %b %d %Y")) #('%Y.%m.%d %H:%M:%S')
                },
            )

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        if message is not None and message != '':
            if self.message_chat.message is None:
                self.message_chat.message = [json.loads(json.dumps(
                    {
                        "message": message,
                        "username": username,
                        "date_public": str((datetime.now()).strftime('%a %b %d %Y')),
                    }
                ))]
                self.message_chat.last_username = username
                self.message_chat.last_message = message
            else:
                self.message_chat.message.append(json.loads(json.dumps(
                    {
                        "message": message,
                        "username": username,
                        "date_public": str((datetime.now()).strftime('%a %b %d %Y')),
                    }
                )))
                self.message_chat.last_username = username
                self.message_chat.last_message = message
                await database_sync_to_async(self.message_chat.save)()
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "username": username,
                        "date_public": str((datetime.now()).strftime('%a %b %d %Y')),
                        # self.message_chat.date_public.strftime("%a %b %d %Y")
                    }
                )
            )

        pass