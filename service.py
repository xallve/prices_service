import asyncio

import pandas
import websockets
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from collections import defaultdict


class CryptoWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.checker = {}
        self.clients = defaultdict(set)

    async def fetch_minute_data(self, symbol):
        pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/USD
        symbol = pair_split[0] + '-' + pair_split[1]
        url = f'https://api.pro.coinbase.com/products/{symbol}/candles?granularity=60'
        response = requests.get(url)
        if response.status_code == 200:  # check to make sure the response from server is good
            data = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])

            return data
        else:
            print("Did not receive OK response from Coinbase API")
            return None

    async def broadcast(self, websocket, symbol):
        while True:
            try:
                data = await self.fetch_minute_data(symbol)
                if data.iloc[0].to_dict() == self.checker:
                    await asyncio.sleep(5)
                elif data is not None:
                    self.checker = data.iloc[0].to_dict()
                    # Getting the latest candle data to return to client
                    await websocket.send(json.dumps(self.checker))
                    # Sleep until next minute
                    await asyncio.sleep(60 - datetime.utcnow().second)
            except Exception as e:
                await websocket.send(json.dumps(self.checker))

    async def handler(self, websocket):
        symbol = "BTC/USD"  # You can change this to any symbol
        await self.broadcast(websocket, symbol)

    async def main(self):
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    server = CryptoWebSocketServer()
    asyncio.run(server.main())
