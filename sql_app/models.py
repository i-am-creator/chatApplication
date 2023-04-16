from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="connections")
'''

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

u = schemas.UserCreate(**{"name": "radhe shyam_1   "})


'''