from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String, default='*****')
    last_active = Column(DateTime, default=None)
    is_active = Column(Boolean, default=True)

    connections = relationship("WsConnection", back_populates="user")


class WsConnection(Base):
    __tablename__ = "ws_connection"

    id_ = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    id = Column(String, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="connections")
    send_messages = relationship("MessageSender", back_populates="sender_con")
    receive_messages = relationship("MessageReceiver", back_populates="receiver_con")


class MessageSender(Base):
    __tablename__ = "message_sender_map"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    message_id = Column(Integer, ForeignKey("message.id"))
    sender_con_id = Column(String, ForeignKey("ws_connection.id"))

    sender_con = relationship("WsConnection", back_populates="send_messages")
    message = relationship("Message", back_populates="sent_by")


class MessageReceiver(Base):
    __tablename__ = "message_receiver_map"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    message_id = Column(Integer, ForeignKey("message.id"))
    receiver_con_id = Column(String, ForeignKey("ws_connection.id"))

    receiver_con = relationship("WsConnection", back_populates="receive_messages")
    message = relationship("Message", back_populates="received_by")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body = Column(String, nullable=False)

    sent_by = relationship("MessageSender", back_populates="message")
    received_by = relationship("MessageReceiver", back_populates="message")
