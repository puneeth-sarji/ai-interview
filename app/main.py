from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import uuid

from app.services.execution import execute_code
from app.services.ai import analyze_code
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="AI-Powered Coding Interview Platform")

class ConnectionManager:
    def __init__(self):
        # room_id -> list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # room_id -> code state
        self.room_code: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            self.room_code[room_id] = "# Write your code here...\n"
        self.active_connections[room_id].append(websocket)
        # Send current code state to new connection
        await websocket.send_text(self.room_code[room_id])

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                del self.room_code[room_id]

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

# Mount static files for the frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Simplistic handling: Assume incoming text is the entire new code state.
            # In a real app, you'd use Operational Transformation or CRDTs.
            if data.startswith("RUN:"):
                language = data.split(":")[1]
                code_to_run = manager.room_code.get(room_id, "")
                output = execute_code(code_to_run, language)
                await manager.broadcast(f"OUTPUT:\n{output}", room_id)
            elif data.startswith("ANALYZE"):
                code_to_analyze = manager.room_code.get(room_id, "")
                feedback = await analyze_code(code_to_analyze)
                await manager.broadcast(f"AI_FEEDBACK:\n{feedback}", room_id)
            else:
                manager.room_code[room_id] = data
                await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
