from starlette.websockets import WebSocket, WebSocketDisconnect
from app.dependencies import ConnectionManager
from fastapi import APIRouter

ws_router = APIRouter(prefix='/ws', tags=['ws'])
manager = ConnectionManager()


@ws_router.get("/{client_id}")
async def websocket_endpoint(client_id: int):
    return client_id


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast_to_others(f"{client_id} : \t\t {data}", websocket)
            # await manager.broadcast(f"{client_id} : \t\t {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
