"""文件映射仓库 - 管理文件ID和文件信息的映射关系"""

from core.crud import CRUDBase
from models.admin import FileMapping


class FileMappingCreate:
    """文件映射创建模型"""

    def __init__(
        self,
        file_id: str,
        original_name: str,
        file_type: str,
        file_size: int | None,
        user_id: int,
        agent_id: int | None = None,
    ):
        self.file_id = file_id
        self.original_name = original_name
        self.file_type = file_type
        self.file_size = file_size
        self.user_id = user_id
        self.agent_id = agent_id


class FileMappingUpdate:
    """文件映射更新模型"""

    pass


class FileMappingRepository(
    CRUDBase[FileMapping, FileMappingCreate, FileMappingUpdate]
):
    """文件映射仓库"""

    async def create_file_mapping(
        self,
        file_id: str,
        original_name: str,
        file_type: str,
        file_size: int | None,
        user_id: int,
        file_path: str | None = None,
    ) -> FileMapping:
        """创建文件映射记录"""
        return await FileMapping.create(
            file_id=file_id,
            original_filename=original_name,
            file_type=file_type,
            file_size=file_size,
            upload_user_id=user_id,
            file_path=file_path,
        )

    async def get_file_info_by_ids(self, file_ids: list[str]) -> list[FileMapping]:
        """根据文件ID列表获取文件信息"""
        if not file_ids:
            return []

        return await FileMapping.filter(file_id__in=file_ids).all()

    async def get_file_mapping_by_file_id(self, file_id: str) -> dict | None:
        """根据文件ID获取文件映射信息"""
        mapping = await FileMapping.filter(file_id=file_id).first()
        if mapping:
            return {
                "file_id": mapping.file_id,
                "original_filename": mapping.original_filename,
                "file_type": mapping.file_type,
                "file_size": mapping.file_size,
                "upload_user_id": mapping.upload_user_id,
                "file_path": mapping.file_path,
            }
        return None


# 全局实例
file_mapping_repository = FileMappingRepository(FileMapping)
