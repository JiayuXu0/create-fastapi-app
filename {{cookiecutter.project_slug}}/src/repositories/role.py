from core.crud import CRUDBase
from models.admin import Api, Menu, Role
from schemas.roles import RoleCreate, RoleUpdate


class RoleRepository(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(model=Role)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def update_roles(
        self, role: Role, menu_ids: list[int], api_infos: list[dict]
    ) -> None:
        # 更新菜单关联
        await role.menus.clear()
        for menu_id in menu_ids:
            menu_obj = await Menu.filter(id=menu_id).first()
            if menu_obj:
                await role.menus.add(menu_obj)

        # 更新API关联
        await role.apis.clear()
        for item in api_infos:
            api_obj = await Api.filter(
                path=item.get("path"), method=item.get("method")
            ).first()
            if api_obj:
                await role.apis.add(api_obj)


role_repository = RoleRepository()
