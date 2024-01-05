import websocket
import json


websocket_url = 'ws://127.0.0.1:8000/ws/messages/'

ws = websocket.WebSocket()
ws.connect(websocket_url)


request_data = {
    'key1': 'value1',
    'key2': 'value2',
}
ws.send(json.dumps(request_data))

response = ws.recv()
print(response)
ws.close()

