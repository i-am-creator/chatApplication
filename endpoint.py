import dotenv
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.routers import ws_router, main_router
from sql_app import models, crud, schemas
from sql_app.database import engine, SessionLocal

dotenv.load_dotenv()

app = FastAPI()

app.mount("/static/", StaticFiles(directory="./"), name="static")
app.include_router(ws_router)
app.include_router(main_router)


@app.on_event("shutdown")
def shutdown_event():
    ## TODO : in case of multiple workers get list of active connections and close them
    db = SessionLocal()
    crud.close_all_connection(db)
    db.close()


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    print('starting up')
    crud.close_all_connection(db)
    db.close()


@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_user(db)
    return users

@app.get("/connections/", response_model=list[schemas.WsConnection])
def read_users(db: Session = Depends(get_db)):
    # users = crud.get_all_connections(db)
    users = crud.get_active_connection_ids(db)
    return users


@app.get("/message/", response_model=list[schemas.Message])
def read_message(db: Session = Depends(get_db)):
    users = crud.get_all_message(db)
    return users

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('endpoint:app', host='localhost', port=8080, reload=False, log_level='info')
