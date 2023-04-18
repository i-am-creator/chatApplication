import datetime

from starlette.websockets import WebSocket

from app.model import User
from sql_app import crud
from sql_app.schemas import UserCreate, WsConnectionCreate, MessageCreate

fake_user_db: list[User] = []


class UserManagement:
    __shared_instance = None
    user_db: list[User] = fake_user_db

    @staticmethod
    def getInstance(db):
        """Static Access Method"""
        if UserManagement.__shared_instance is None:
            UserManagement(db)
        return UserManagement.__shared_instance

    def __init__(self, db):
        """virtual private constructor"""
        self.db = db
        if UserManagement.__shared_instance is not None:
            raise Exception("This class is a singleton class !")
        else:
            UserManagement.__shared_instance = self

    @property
    def get_all_user(self):
        return self.user_db

    @property
    def get_active_user(self):
        return [u for u in self.user_db if u.is_active]

    @property
    def get_active_connections(self):
        # return [u.current_connection for u in self.user_db if u.is_active]
        return crud.get_active_connection_ids(self.db)

    def get_user_by_connection_id(self, connection_id):
        for u in self.user_db:
            if u.connection_id == connection_id:
                return u.__dict__

    def get_user_name_by_id(self, connection_id):
        for u in self.user_db:
            if u.connection_id == connection_id:
                return u.name

    def connect_user(self, websocket: WebSocket, connection_id, username):
        db_user = crud.get_user_by_name(self.db, username)
        if not db_user:
            user = UserCreate(**{'name': username})
            db_user = crud.create_user(self.db, user)

        conn = WsConnectionCreate(**{'id': connection_id})
        connection = crud.create_connection(self.db, conn, user_id=db_user.id)
        return connection.id

    def disconnect_user(self, connection_id):
        crud.close_connection(self.db, connection_id)
        return crud.get_user_by_cid(self.db, connection_id)


class MessageManagement:
    __shared_instance = None
    user_db: list[User] = fake_user_db

    @staticmethod
    def getInstance(db):
        """Static Access Method"""
        if MessageManagement.__shared_instance is None:
            MessageManagement(db)
        return MessageManagement.__shared_instance

    def __init__(self, db):
        """virtual private constructor"""
        self.db = db
        if MessageManagement.__shared_instance is not None:
            raise Exception("This class is a singleton class !")
        else:
            MessageManagement.__shared_instance = self

    def createMessage(self, body: str, send_by: int):
        message = MessageCreate(**{"body": body})
        message = crud.create_message(self.db, message)
        crud.create_sender(self.db, message.id, send_by)
        return message

    def createMessageReceiver(self, message_id: int, received_by: int):
        return crud.create_receiver(self.db, message_id, received_by)
