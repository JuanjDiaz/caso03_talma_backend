from abc import ABC, abstractmethod

from app.modules.security.domain import Usuario
from app.dto.universal_dto import BaseOperacionResponse
from app.dto.usuario_dtos import UsuarioCambioPasswordRequest, UsuarioRequest, UsuarioFiltroRequest, UsuarioFiltroResponse
from app.dto.collection_response import CollectionResponse


class UsuarioService(ABC):
    
    @abstractmethod
    async def saveOrUpdate(self, request: UsuarioRequest) -> None:
        pass

    @abstractmethod
    async def get(self, usuarioId: str) -> Usuario:
        pass

    @abstractmethod
    async def find(self, request: UsuarioFiltroRequest) -> CollectionResponse[UsuarioFiltroResponse]:
        pass

    @abstractmethod
    async def updatePassword(self, request: UsuarioCambioPasswordRequest):
        pass