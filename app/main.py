from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.ws.websocket_handler import websocket_endpoint

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/query")
async def query_ws(websocket: WebSocket):
    await websocket_endpoint(websocket)
