import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TelegramUser

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self)
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        print('asssssssaaaa')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )
    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        #send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

    pass

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected')
        # print(self.scope["url_route"]["kwargs"]["chat_box_name"])
        # print(self.scope)
        # Called when the WebSocket handshake is successful
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name
        # self.group_name = "message_1100"
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnected')
        # Called when the WebSocket connection is closed
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        

    async def receive(self, text_data):
        print('receive')
        # Called when a message is received from the WebSocket
        text_data_json = json.loads(text_data)
        # print(text_data_json,'weebbbssss')
        chat_id = text_data_json['chat_id']
        message_id = text_data_json['message_id']
        user_id = text_data_json['user_id']
        text = text_data_json['text']
        owner = text_data_json['owner']
        image = text_data_json['image']
        username = text_data_json['username']
        msg_type = text_data_json['msg_type']
        file = text_data_json['file']

        # Process the message and prepare the response
        
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "chat_id": chat_id,
                "message_id": message_id,
                "user_id": user_id,
                "text": text,
                "owner": owner,
                "image":image,
                "username":username,
                "msg_type":msg_type,
                "file":file
            },
        )

        # Send the response back to the connected client
        # print(response_message)
        # await self.send(text_data=json.dumps({'message': response_message}))
        # print(self)
    async def chatbox_message(self, event):
       
        chat_id = event["chat_id"]
        message_id = event["message_id"]
        user_id = event["user_id"]
        text = event["text"]
        owner = event["owner"]
        image = event["image"]
        username = event["username"]
        msg_type = event["msg_type"]
        file = event["file"]

        
        await self.send(
            text_data=json.dumps(
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "user_id": user_id,
                    "text": text,
                    "owner": owner,
                    "image":image,
                    "username":username,
                    "msg_type":msg_type,
                    "file":file
                }
            )
        )