from abc import  abstractmethod
from app.modules.integration.base_repository import BaseRepository
from app.modules.security.domain import Usuario
from app.modules.security.domain.VwUsuario import VwUsuario
from app.dto.collection_response import CollectionResponse
from app.dto.usuario_dtos import UsuarioFiltroRequest, UsuarioResponse
from typing import Tuple, List



class UsuarioRepository(BaseRepository[Usuario]):

    @abstractmethod
    async def save_or_update(self, t: Usuario) -> bool:
        pass

    @abstractmethod
    async def  get(self, usuarioId:str) -> Usuario:
        pass

    @abstractmethod
    async def find(self, request: UsuarioFiltroRequest) -> Tuple[List[VwUsuario], int]:
        pass

    
  