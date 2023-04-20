from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from app.dependencies import Connection
from app.dependencies import get_db

ws_router = APIRouter(prefix='/ws', tags=['ws'])


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, username: str = 'Creator',
                             db: Session = Depends(get_db)):
    print(username)
    conection = Connection(db, websocket, client_id, username)
    await conection.connect()
