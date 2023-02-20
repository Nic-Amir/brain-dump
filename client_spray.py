import websocket
import json

def on_message(ws, message):
    sprayed_number = json.loads(message)['sprayed_number']
    print(f'Sprayed number: {sprayed_number:.2f}')

if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect('ws://localhost:5000/spray')
    ws.on_message = on_message

    try:
        while True:
            # Send an empty message to the server to trigger the server to send a random number
            ws.send('')
    except KeyboardInterrupt:
        ws.close()
