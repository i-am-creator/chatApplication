from starlette.websockets import WebSocket, WebSocketDisconnect
from app.dependencies import Connection
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ws_router = APIRouter(prefix='/ws', tags=['ws'])


# manager = ConnectionManager()


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, username: str = 'Creator',
                             db: Session = Depends(get_db)):
    print(username)
    conection = Connection(db, websocket, client_id, username)
    await conection.connect()
