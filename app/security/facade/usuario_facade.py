from abc import ABC, abstractmethod

from dto.universal_dto import BaseOperacionResponse
from dto.usuario_dtos import UsuarioRequest


class UsuarioFacade(ABC):
    
    @abstractmethod
    async def saveOrUpdate(self, request: UsuarioRequest) -> BaseOperacionResponse:
        pass

