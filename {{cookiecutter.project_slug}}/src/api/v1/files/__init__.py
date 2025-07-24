from fastapi import APIRouter

from .files import router

files_router = APIRouter()
files_router.include_router(router, tags=["上传文件"])

__all__ = ["files_router"]
