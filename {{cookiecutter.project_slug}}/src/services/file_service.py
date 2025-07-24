"""文件服务层 - 统一文件处理业务逻辑"""

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from core.ctx import CTX_USER_ID
from log import logger
from repositories.file_mapping import file_mapping_repository
from repositories.user import user_repository
from schemas.base import Success

# 文件安全配置
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
UPLOADS_DIR = "uploads"

ALLOWED_EXTENSIONS: set[str] = {
    # 文档类型
    ".txt",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    # 图片类型
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".svg",
    # 音视频类型
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".m4a",
    ".mp4",
    ".avi",
    ".mkv",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    # 其他文件类型
    ".json",
    ".xml",
    ".csv",
    ".zip",
    ".rar",
    ".7z",
}

DANGEROUS_EXTENSIONS: set[str] = {
    ".exe",
    ".bat",
    ".cmd",
    ".com",
    ".pif",
    ".scr",
    ".vbs",
    ".js",
    ".jar",
    ".sh",
    ".ps1",
    ".php",
    ".asp",
    ".jsp",
    ".py",
    ".pl",
    ".rb",
}


class FileService:
    """文件服务类 - 专门处理文件上传和安全验证逻辑"""

    def __init__(self):
        self.logger = logger
        # 确保上传目录存在
        self.uploads_dir = Path(UPLOADS_DIR)
        self.uploads_dir.mkdir(exist_ok=True)

    async def upload_file(self, file: UploadFile) -> Success:
        """
        通用文件上传

        Args:
            file: 上传的文件

        Returns:
            Success: 上传结果响应
        """
        try:
            # 用户身份验证
            user = await self._authenticate_user()

            # 文件安全验证
            self._validate_file_security(file)

            # 生成安全文件名
            safe_filename = self._generate_safe_filename(file.filename)

            # 读取并验证文件内容
            content = await self._read_and_validate_file(file)

            # 生成文件ID和保存路径
            file_id = str(uuid.uuid4())
            file_path = self.uploads_dir / f"{file_id}_{safe_filename}"

            # 保存文件到本地
            with open(file_path, "wb") as f:
                f.write(content)

            self.logger.info(f"文件已保存: {file_path}")

            # 保存文件映射信息
            await self._save_file_mapping(
                {"file_id": file_id, "file_path": str(file_path)}, file, user.id
            )

            # 返回文件信息
            response_data = {
                "file_id": file_id,
                "original_filename": file.filename,
                "file_type": self._determine_file_type(file.filename),
                "file_size": len(content),
                "file_path": str(file_path),
            }

            return Success(
                data=response_data,
                msg="文件上传成功",
            )

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"文件上传失败: {str(e)}")
            raise HTTPException(status_code=500, detail="文件上传失败") from e

    async def _authenticate_user(self):
        """验证用户身份"""
        user_id = CTX_USER_ID.get()
        if not user_id:
            raise HTTPException(status_code=401, detail="用户未认证")

        user = await user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        return user

    def _validate_file_security(self, file: UploadFile) -> None:
        """验证文件安全性"""
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名不能为空")

        # 获取文件扩展名
        file_ext = Path(file.filename).suffix.lower()

        # 检查危险文件类型
        if file_ext in DANGEROUS_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail=f"不允许上传的文件类型: {file_ext}"
            )

        # 检查是否在允许的扩展名列表中
        if file_ext and file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {file_ext}，允许的类型: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            )

    def _generate_safe_filename(self, original_filename: str) -> str:
        """生成安全的文件名（防止路径遍历攻击）"""
        file_ext = Path(original_filename).suffix.lower()
        return f"{uuid.uuid4().hex}{file_ext}"

    async def _read_and_validate_file(self, file: UploadFile) -> bytes:
        """读取并验证文件内容"""
        content = await file.read()

        # 验证文件大小
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制 {MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        return content

    async def _save_file_mapping(
        self,
        response_data: dict,
        file: UploadFile,
        user_id: int,
    ) -> None:
        """保存文件映射信息"""
        try:
            # 从响应中获取文件ID
            file_id = response_data.get("file_id")
            if not file_id:
                self.logger.warning("无法从响应中获取文件ID")
                return

            # 确定文件类型
            file_type = self._determine_file_type(file.filename)

            # 获取文件大小
            file_size = file.size if hasattr(file, "size") else None

            # 保存文件映射
            await file_mapping_repository.create_file_mapping(
                file_id=file_id,
                original_name=file.filename,
                file_type=file_type,
                file_size=file_size,
                user_id=user_id,
                file_path=response_data.get("file_path"),  # 存储本地文件路径
            )

            self.logger.info(f"已保存文件映射: {file_id} -> {file.filename}")

        except Exception as e:
            # 文件映射保存失败不应该影响上传流程
            self.logger.warning(f"保存文件映射失败: {str(e)}")

    def _determine_file_type(self, filename: str) -> str:
        """确定文件类型"""
        if not filename:
            return "unknown"

        file_ext = filename.lower().split(".")[-1] if "." in filename else ""

        # 图片类型
        image_exts = ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"]
        # 音频类型
        audio_exts = ["mp3", "wav", "flac", "aac", "ogg", "m4a"]
        # 视频类型
        video_exts = ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"]

        if file_ext in image_exts:
            return "image"
        elif file_ext in audio_exts:
            return "audio"
        elif file_ext in video_exts:
            return "video"
        else:
            return "document"


# 全局实例
file_service = FileService()
