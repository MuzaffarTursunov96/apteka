import aiohttp
import asyncio

async def connect_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://54.210.252.107:8001/ws/messages/3/') as ws:
        # async with session.ws_connect('ws://127.0.0.1:8000/ws/messages/3/') as ws:
            # Perform actions with the WebSocket connection
            message_data = {
            "chat_id": '3',
            "message_id": '45',
            "user_id": 3,
            "text": 'salom',
            "owner": '3',
            "image": '',
            "username": 'Muzaffar',
            "msg_type": 'text',
            "file": ''
            }
            await ws.send_json(message_data)
            # await self.send(text_data=json.dumps(message_data))
            
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f'Received message: {msg.data}')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f'WebSocket connection closed with exception: {ws.exception()}')
                    
asyncio.run(connect_websocket())