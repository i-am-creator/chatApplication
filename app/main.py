import dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import ws_router, main_router

dotenv.load_dotenv()


app = FastAPI()

app.mount("/static/", StaticFiles(directory="./"), name="static")
app.include_router(ws_router)
app.include_router(main_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='localhost', port=8080, reload=True, log_level='info')
