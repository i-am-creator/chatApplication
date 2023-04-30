from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.dependencies.db import UserManagement, MessageManagement

CONNECTION_ID_OBJECT_MAP = {}


class ConnectionManager:
    def __init__(self, db):
        self.user_db_manager: UserManagement = UserManagement.getInstance(db)
        self.message_db_manager: MessageManagement = MessageManagement.getInstance(db)

    def connect(self, websocket: WebSocket, client_id, username):
        connection_id = self.user_db_manager.connect_user(websocket, client_id, username)
        CONNECTION_ID_OBJECT_MAP[connection_id] = websocket

    async def disconnect(self, client_id):
        user = self.user_db_manager.disconnect_user(connection_id=client_id)
        print(f"{user.name} left the chat", CONNECTION_ID_OBJECT_MAP.get(client_id, None))
        CONNECTION_ID_OBJECT_MAP.pop(str(client_id), None)
        await self.broadcast(f"{user.name} left the chat")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection_id in CONNECTION_ID_OBJECT_MAP.keys():
            connection = CONNECTION_ID_OBJECT_MAP.get(connection_id, None)
            if connection:
                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    CONNECTION_ID_OBJECT_MAP.pop(connection_id, None)

    async def broadcast_to_others(self, message: str, websocket: WebSocket):
        for connection_id in CONNECTION_ID_OBJECT_MAP.keys():
            connection = CONNECTION_ID_OBJECT_MAP.get(connection_id, None)
            if connection and connection != websocket:

                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    CONNECTION_ID_OBJECT_MAP.pop(connection_id, None)

    async def broadcast_to(self, message: str, connection_id: str):
        connection = CONNECTION_ID_OBJECT_MAP.get(connection_id, None)
        if connection:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                pass
                CONNECTION_ID_OBJECT_MAP.pop(connection_id, None)

    async def message_received(self, message, by):
        db_message = self.message_db_manager.createMessage(body=message, send_by=by.client_id)

        for connection in self.user_db_manager.get_active_connections:
            connection_id = connection.id
            if int(connection_id) == by.client_id:
                message_to_others = '{}\t:\t\t\t\t{}'.format("You ", message)
                await self.broadcast_to(message_to_others, connection_id)
            else:
                message_to_others = '{}\t:\t\t\t\t{}'.format(by.client_name, message)
                self.message_db_manager.createMessageReceiver(db_message.id, received_by=connection_id)
                await self.broadcast_to(message_to_others, connection_id)


class Connection:
    def __init__(self, db, websocket, client_id, username):
        self.ws = websocket
        self.client_id = client_id
        self.client_name = username
        self.connection_manager = ConnectionManager(db)

    async def connect(self):
        await self.ws.accept()
        self.connection_manager.connect(self.ws, self.client_id, self.client_name)
        await self.connection_manager.send_personal_message(f"Welcome {self.client_name} !! ", self.ws)
        await self.connection_manager.broadcast_to_others(f"{self.client_name} joined the chat", self.ws)

        try:
            while True:
                data = await self.ws.receive_text()
                await self.connection_manager.message_received(message=data, by=self)
                # await self.connection_manager.send_personal_message(f"You wrote: {data}", self.ws)
                # await self.connection_manager.broadcast_to_others(f"{self.client_name} : \t\t {data}", self.ws)

        except WebSocketDisconnect:
            await self.connection_manager.disconnect(self.client_id)
