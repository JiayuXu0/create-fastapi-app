from typing import Optional

from core.crud import CRUDBase
from models.admin import Menu
from schemas.menus import MenuCreate, MenuUpdate


class MenuRepository(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def __init__(self):
        super().__init__(model=Menu)

    async def get_by_menu_path(self, path: str) -> Optional["Menu"]:
        return await self.model.filter(path=path).first()


menu_repository = MenuRepository()
