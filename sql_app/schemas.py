from typing import Union

from pydantic import BaseModel


class WsConnectionBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BaseMessage(BaseModel):
    body: str

    class Config:
        orm_mode = True


class WsConnectionCreate(WsConnectionBase):
    id: int


class UserCreate(UserBase):
    password: str = '****************'


class FakeUserBase(UserBase):
    class Config:
        orm_mode = True


class FakeMessageBase(BaseMessage):
    body: str

    class Config:
        orm_mode = True


class MessageSender(BaseModel):
    message: FakeMessageBase

    class Config:
        orm_mode = True


class MessageReceiver(BaseModel):
    message: FakeMessageBase

    class Config:
        orm_mode = True


class WsConnection(WsConnectionBase):
    id: int
    user_id: int
    is_active: bool

    user: FakeUserBase
    send_messages: list[MessageSender]
    receive_messages: list[MessageReceiver]

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool
    connections: list[WsConnection] = []

    class Config:
        orm_mode = True


class MessageCreate(BaseMessage):
    pass


class Message(BaseMessage):
    id: int

    class Config:
        orm_mode = True
