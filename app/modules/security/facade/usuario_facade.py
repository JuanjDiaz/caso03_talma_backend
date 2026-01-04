from abc import ABC, abstractmethod

from app.dto.collection_response import CollectionResponse
from app.dto.universal_dto import BaseOperacionResponse
from app.dto.usuario_dtos import UsuarioCambioPasswordRequest, UsuarioComboResponse, UsuarioFiltroRequest, UsuarioRequest, UsuarioResponse, UsuarioFiltroResponse, UsuarioStatusRequest


class UsuarioFacade(ABC):
    
    @abstractmethod
    async def saveOrUpdate(self, request: UsuarioRequest) -> BaseOperacionResponse:
        pass

    @abstractmethod
    async def get(self, usuarioId: str) -> UsuarioResponse:
        pass

    @abstractmethod
    async def  find(self, request: UsuarioFiltroRequest) -> CollectionResponse[UsuarioFiltroResponse]:
        pass

    @abstractmethod
    async def init(self) -> UsuarioComboResponse:
        pass

    @abstractmethod
    async def changeStatus(self, t: UsuarioStatusRequest) -> BaseOperacionResponse:
        pass

    @abstractmethod
    async def initForm(self) -> UsuarioComboResponse:
        pass

    @abstractmethod
    async def updatePassword(self, request: UsuarioCambioPasswordRequest) -> BaseOperacionResponse:
        pass
