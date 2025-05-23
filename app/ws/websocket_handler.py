from fastapi import WebSocket, WebSocketDisconnect
from app.models.models import QueryRequest, QueryResponse
from app.engine.rag_engine import process_query
import json

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            req = QueryRequest.parse_raw(data)
            answer, context = process_query(req.query)
            res = QueryResponse(answer=answer, context=context)
            await websocket.send_text(res.json())
    except WebSocketDisconnect:
        print("🔌 Client disconnected")
    except Exception as e:
        print(f"🔥 Unexpected error: {e}")
        try:
            await websocket.send_text(json.dumps({"error": str(e)}))
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass
