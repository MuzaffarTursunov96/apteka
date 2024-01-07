import websocket
import json

#curl -F "url=https://mdm.akfagroup.com" "https://api.telegram.org/6918479750:AAFm4eunDMv6IHZaAHv7w_YDup-VSL7YhHA/setWebhook"


websocket_url = 'ws://127.0.0.1:8000/ws/messages/1/'

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

