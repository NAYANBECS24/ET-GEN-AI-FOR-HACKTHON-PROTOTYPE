from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, payload: dict) -> None:
        dead: list[WebSocket] = []
        for conn in self.connections:
            try:
                await conn.send_json(payload)
            except Exception:
                dead.append(conn)
        for conn in dead:
            self.disconnect(conn)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_updates(websocket: WebSocket):
    await manager.connect(websocket)
    await websocket.send_json({"message": "connected", "channel": "aegis-events"})
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast({"echo": data, "type": "runtime-update"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
