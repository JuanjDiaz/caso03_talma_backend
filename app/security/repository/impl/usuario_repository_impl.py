
from app.integration.impl.base_repository_impl import BaseRepositoryImpl
from app.security.domain import Usuario
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.repository.usuario_repository import UsuarioRepository


class UsuarioRepositoryImpl(BaseRepositoryImpl[Usuario], UsuarioRepository):
    
    def __init__(self, db: AsyncSession):
        super().__init__(Usuario, db)


    async def save_or_update(self, t: Usuario) -> bool:
        try:
            resultado = await self.save(t)
            return resultado is not None
        except Exception as e: 
            return False
        