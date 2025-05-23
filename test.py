import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8000/ws/query"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"query": "What is PMT Pro?"}))
        response = await ws.recv()
        print("Response:", json.loads(response))

asyncio.run(test())
