import asyncio
import websockets
import json

async def receive_data():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print("Received data:", data)

if __name__ == "__main__":
    asyncio.run(receive_data())