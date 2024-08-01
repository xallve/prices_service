import asyncio
import time

import websockets
import json

async def fetch_data():
    uri = "ws://localhost:8765"  # Адрес вашего WebSocket сервера
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            data = json.loads(message)
            yield data

async def process_data():
    async for data in fetch_data():
        print("Received data:", data)

if __name__ == "__main__":
    asyncio.run(process_data())
