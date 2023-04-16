import datetime
from typing import Optional,  Union

from fastapi import WebSocket
from pydantic import BaseModel


class User():
    name: str = ""
    last_active: datetime.datetime = datetime.datetime.now()
    id: Union[str, int] = ''
    password: str = '**************'
    current_connection: Optional[WebSocket] = None
    prev_connection_id: list[int] = []
    is_active: bool = False

    def __init__(self,current_connection:WebSocket):
        self.current_connection = current_connection

