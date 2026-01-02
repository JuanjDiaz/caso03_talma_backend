from typing import List
from app.modules.security.domain import Rol
from app.modules.security.service.rol_service import RolService


from app.modules.security.repository.rol_repository import RolRepository


class RolServiceImpl(RolService):

    def __init__(self, rol_repository: RolRepository):
        self.rol_repository = rol_repository

    async def load(self) -> List[Rol]:
        return await self.rol_repository.load()