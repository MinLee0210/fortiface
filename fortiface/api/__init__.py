from fastapi import APIRouter

from fortiface.api.routers import recognition_router, register_router

api_router = APIRouter()

api_router.include_router(recognition_router.router, prefix="", tags=["process"])
api_router.include_router(register_router.router, prefix="register", tags=["process"])
