import os

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from app.dependencies import templates

main_router = APIRouter(tags=['web app'])


@main_router.get('/')
async def get():
    response = RedirectResponse(url='/app')
    return response
