from sqlalchemy.orm import Session

from . import models, schemas


def get_all_user(db: Session):
    return db.query(models.User).all()


def get_all_connections(db: Session):
    return db.query(models.WsConnection).all()


#
# def get_all_map(db: Session):
#     return db.query(models.MessageSenderReceiver).all()


def get_all_message(db: Session):
    return db.query(models.Message).all()


def get_active_user(db: Session):
    return db.query(models.User).filter(models.User.is_active).all()


def get_active_connection_ids(db: Session):
    return db.query(models.WsConnection).filter(models.WsConnection.is_active==True).all()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_cid(db: Session, connection_id: int):
    return db.query(models.User).filter(models.WsConnection.user_id == models.User.id,
                                        models.WsConnection.id == connection_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(name=user.name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_connection(db: Session, conn: schemas.WsConnectionCreate, user_id: int):
    db_item = models.WsConnection(**conn.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_message(db: Session, message: schemas.MessageCreate):
    db_item = models.Message(**message.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_sender(db: Session, message_id: int, connection_id: int):
    db_item = models.MessageSender(**{"message_id": message_id, "sender_con_id": connection_id})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_receiver(db: Session, message_id: int, connection_id: int):
    db_item = models.MessageReceiver(**{"message_id": message_id, "receiver_con_id": connection_id})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def close_all_connection(db: Session):
    db.query(models.WsConnection).update({models.WsConnection.is_active: False}, synchronize_session=False)
    db.commit()


def close_connection(db: Session, connection_id: int):
    k = db.query(models.WsConnection).filter(models.WsConnection.id == connection_id).update(
        {models.WsConnection.is_active: False}, synchronize_session=False)
    db.commit()
