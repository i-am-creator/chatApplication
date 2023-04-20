from fastapi.templating import Jinja2Templates
from sql_app.database import SessionLocal, engine

templates = Jinja2Templates(directory="./html-template")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
