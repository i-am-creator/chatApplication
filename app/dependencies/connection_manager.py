import datetime

from fastapi import WebSocket

from app.model import User
from app.dependencies.db import user_db

class ConnectionManager:

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        user = User(current_connection=websocket)
        user.is_active = True
        user.id = client_id
        user_db.append(user)

    def disconnect(self, websocket: WebSocket):
        for i in range(len(user_db)):
            if user_db[i].current_connection == websocket:
                user_db[i].is_active = False
                user_db[i].last_active = datetime.datetime.now()
                user_db[i].prev_connection_id.append(websocket.user)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for user in user_db:
            if user.is_active:
                await user.current_connection.send_text(message)

    async def broadcast_to_others(self, message: str, websocket: WebSocket):
        for user in user_db:
            if user.current_connection != websocket and user.is_active:
                await user.current_connection.send_text(message)
