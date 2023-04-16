import datetime

from starlette.websockets import WebSocket

from app.model import User

fake_user_db: list[User] = []


class UserManagement:
    __shared_instance = None
    user_db: list[User] = fake_user_db

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if UserManagement.__shared_instance is None:
            UserManagement()
        return UserManagement.__shared_instance

    def __init__(self):
        """virtual private constructor"""
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
        return [u.current_connection for u in self.user_db if u.is_active]

    def get_user_by_connection_id(self, connection_id):
        for u in self.user_db:
            if u.connection_id == connection_id:
                return u.__dict__

    def get_user_name_by_id(self, connection_id):
        for u in self.user_db:
            if u.connection_id == connection_id:
                return u.name


    def connect_user(self, websocket: WebSocket, connection_id, username):
        user_exists = False
        for i in range(len(self.user_db)):
            if self.user_db[i].name == username:
                self.user_db[i].current_connection = websocket
                self.user_db[i].connection_id = connection_id
                self.user_db[i].is_active = True
                self.user_db[i].last_active = datetime.datetime.now()
                user_exists = True
        if not user_exists:
            user = User(current_connection=websocket)
            user.is_active = True
            user.connection_id = connection_id
            user.name = username
            self.user_db.append(user)



    def disconnect_user(self, connection_id):
        for i in range(len(self.user_db)):
            if self.user_db[i].connection_id == connection_id:
                # self.user_db[i].connection_id = None
                self.user_db[i].current_connection = None
                self.user_db[i].is_active = False
                self.user_db[i].last_active = datetime.datetime.now()
                self.user_db[i].prev_connection_id.append(connection_id)





