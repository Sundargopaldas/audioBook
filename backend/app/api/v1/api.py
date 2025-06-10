from fastapi import APIRouter
from app.api.v1.endpoints import audiobooks

api_router = APIRouter()

api_router.include_router(audiobooks.router, prefix="/audiobooks", tags=["audiobooks"])