from abc import ABC, abstractmethod

from dto.universal_dto import ComboBaseResponse


class ComunFacade(ABC):

    @abstractmethod
    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> ComboBaseResponse:
        pass

    @abstractmethod
    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> ComboBaseResponse:
        pass