from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.dependencies.db import UserManagement


class ConnectionManager:
    user_db_manager: UserManagement = UserManagement.getInstance()

    def connect(self, websocket: WebSocket, client_id, username):
        self.user_db_manager.connect_user(websocket, client_id, username)

    async def disconnect(self, websocket: WebSocket, client_id):
        self.user_db_manager.disconnect_user(connection_id=client_id)
        await self.broadcast_to_others(f"Client #{client_id} left the chat", websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.user_db_manager.get_active_connections:
            if connection:
                await connection.send_text(message)

    async def broadcast_to_others(self, message: str, websocket: WebSocket):
        for connection in self.user_db_manager.get_active_connections:
            if connection != websocket:
                await connection.send_text(message)


class Connection:
    def __init__(self, websocket, client_id, username):
        self.ws = websocket
        self.client_id = client_id
        self.client_name = username
        self.connection_manager = ConnectionManager()

    async def connect(self):
        await self.ws.accept()
        self.connection_manager.connect(self.ws, self.client_id, self.client_name)
        await self.connection_manager.send_personal_message(f"Welcome {self.client_name} !! ", self.ws)
        await self.connection_manager.broadcast_to_others(f"Client #{self.client_name} joined the chat", self.ws)

        try:
            while True:
                data = await self.ws.receive_text()
                await self.connection_manager.send_personal_message(f"You wrote: {data}", self.ws)
                await self.connection_manager.broadcast_to_others(f"{self.client_name} : \t\t {data}", self.ws)

        except WebSocketDisconnect:
            await self.connection_manager.disconnect(self.ws, self.client_id)
