import os

from fastapi import APIRouter, Request
from app.dependencies import templates

main_router = APIRouter(tags=['web app'])


@main_router.get('/')
async def get(request: Request):
    print("ENV: ", os.getenv('WebSocketURL', 'ws://localhost:8000/ws'))
    return templates.TemplateResponse("main_page.html",
                                      {"request": request,
                                       "WebSocketURL": os.getenv('WebSocketURL', 'ws://localhost:8000/ws')
                                       }
                                      )
