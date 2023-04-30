import datetime
from typing import Optional, Union, List

from fastapi import WebSocket
from pydantic import BaseModel


class Connections:
    user_id: int
    connection_id: int
    connection: Optional[WebSocket] = None


class Msg:
    sender : int


class User:
    name: str = ""
    last_active: datetime.datetime = datetime.datetime.now()
    id: Union[str, int] = ''
    password: str = '***'
    current_connection: Optional[WebSocket] = None
    is_active: bool = False
    connection_id = None

    prev_connection_id: List[int] = []

    def __init__(self,current_connection:WebSocket):
        self.current_connection = current_connection

