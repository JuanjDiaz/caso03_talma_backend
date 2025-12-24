import logging
from app.integration.impl.base_repository_impl import BaseRepositoryImpl
from app.security.domain import Usuario
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.repository.usuario_repository import UsuarioRepository
from core.exceptions import NotFoundException

logger = logging.getLogger(__name__)

class UsuarioRepositoryImpl(BaseRepositoryImpl[Usuario], UsuarioRepository):
    
    def __init__(self, db: AsyncSession):
        super().__init__(Usuario, db)


    async def save_or_update(self, t: Usuario) -> bool:
        try:
            resultado = await self.save(t)
            return resultado is not None
        except Exception as e: 
            logger.error(f"Error saving user: {e}", exc_info=True)
            return False
        
    async def  get(self, usuarioId:str) -> Usuario:
        try: 
            usuario = await self.get_by_id(usuarioId)
            if not usuario:
                raise NotFoundException("Usuario no encontrado")
            return usuario
        except Exception as e: 
            logger.error(f"Error getting user {usuarioId}: {e}", exc_info=True)
            raise NotFoundException("Usuario no encontrado")