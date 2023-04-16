from starlette.websockets import WebSocket, WebSocketDisconnect
from app.dependencies import ConnectionManager, Connection
from fastapi import APIRouter

ws_router = APIRouter(prefix='/ws', tags=['ws'])
manager = ConnectionManager()


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, username: str = 'Creator'):
    print(username)
    conection = Connection(websocket, client_id, username)
    await conection.connect()
