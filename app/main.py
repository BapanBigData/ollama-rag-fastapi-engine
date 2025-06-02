# import sys
# import pysqlite3
# sys.modules["sqlite3"] = pysqlite3

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.ws.websocket_handler import websocket_endpoint
from app.engine.bootstrap import build_vector_store_if_needed

# ✅ Use lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run once at startup
    build_vector_store_if_needed()
    yield
    # Run once at shutdown (optional cleanup logic here)

app = FastAPI(lifespan=lifespan)

# CORS middleware
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
