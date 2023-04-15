import datetime
import os
from typing import Union

import dotenv

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

dotenv.load_dotenv()
app = FastAPI()
app.mount("/static/", StaticFiles(directory="./"), name="static")
templates = Jinja2Templates(directory="./html-template")


class User:
    def __init__(self, current_connection):
        self.name: str = ""
        self.last_active: datetime.datetime = datetime.datetime.now()
        self.id: Union[str, int] = ''
        self.password: str = '**************'
        self.current_connection: WebSocket = current_connection
        self.prev_connection_id: list[int] = []
        self.is_active: bool = False


user_db: list[User] = []


class ConnectionManager:

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        global user_db
        user = User(current_connection=websocket)
        user.is_active = True
        user.id = client_id
        user_db.append(user)

    def disconnect(self, websocket: WebSocket):
        global user_db
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


manager = ConnectionManager()


@app.get("/")
async def get(request: Request):
    print("ENV: ", os.getenv('WebSocketURL', 'ws://localhost:8000/ws'))
    return templates.TemplateResponse("main_page.html",
                                      {"request": request,
                                       "WebSocketURL": os.getenv('WebSocketURL', 'ws://localhost:8000/ws')
                                       }
                                      )


@app.websocket("/ws/{client_id}")
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app.main:app', host='localhost', port=8080, reload=True)
