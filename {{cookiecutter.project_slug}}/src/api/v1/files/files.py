from fastapi import APIRouter, File, UploadFile

from core.dependency import DependAuth
from services.file_service import file_service

router = APIRouter()


@router.post(
    "/upload",
    summary="上传文件",
    dependencies=[DependAuth],
)
async def upload_file(
    file: UploadFile = File(..., description="要上传的文件"),
):
    """
    通用文件上传

    Args:
        file: 上传的文件

    Returns:
        上传成功的响应，包含文件信息
    """
    return await file_service.upload_file(file)
