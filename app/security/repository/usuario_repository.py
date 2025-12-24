from abc import  abstractmethod
from app.integration.base_repository import BaseRepository
from app.security.domain import Usuario


class UsuarioRepository(BaseRepository[Usuario]):

    @abstractmethod
    async def save_or_update(self, t: Usuario) -> bool:
        pass

  