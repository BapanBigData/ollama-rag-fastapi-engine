import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8000/ws/query"
    async with websockets.connect(
        uri,
        ping_interval=30,    # Send a ping every 30 seconds
        ping_timeout=(120*2)     # Wait up to 4 minutes before considering it dead
    ) as ws:
        await ws.send(json.dumps({"query": "List all the important features to remember of PMT Pro."}))
        response = await ws.recv()
        print("Response:", json.loads(response))

asyncio.run(test())
