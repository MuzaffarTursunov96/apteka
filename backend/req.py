import aiohttp
import asyncio

async def connect_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:8000/ws/messages') as ws:
            # Perform actions with the WebSocket connection
            await ws.send_str('Hello, WebSocket!')
            
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f'Received message: {msg.data}')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f'WebSocket connection closed with exception: {ws.exception()}')
                    
asyncio.run(connect_websocket())