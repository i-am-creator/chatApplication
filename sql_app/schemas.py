from typing import Union

from pydantic import BaseModel


class WsConnectionBase(BaseModel):
    pass


class WsConnectionCreate(WsConnectionBase):
    id: int


class WsConnection(WsConnectionBase):
    id: int
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str = '****************'


class User(UserBase):
    id: int
    is_active: bool
    connections: list[WsConnection] = []

    class Config:
        orm_mode = True
