from typing import List
from app.integration.impl.base_repository_impl import BaseRepositoryImpl
from app.security.domain import Rol, Usuario
from sqlalchemy.ext.asyncio import AsyncSession
from app.security.repository.rol_repository import RolRepository
from app.security.repository.usuario_repository import UsuarioRepository






class RolRepositoryImpl(BaseRepositoryImpl[Rol], RolRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(Rol, db)

    async def load(self) -> List[Rol]:
        return await self.get_all()