from abc import ABC, abstractmethod
from typing import Any
from app.modules.analysis.domain.guia_aerea import GuiaAerea
from app.dto.guia_aerea_dtos import  GuiaAereaFiltroRequest, GuiaAereaRequest


class DocumentService(ABC):

    @abstractmethod
    async def saveOrUpdate(self, request: GuiaAereaRequest):
        pass

    @abstractmethod
    async def get(self, documentoId: str) -> GuiaAerea:
        pass

    @abstractmethod
    async def find(self, request: GuiaAereaFiltroRequest) -> tuple[Any, int]:
        pass

    @abstractmethod
    async def get_with_relations(self, documentoId: str) -> GuiaAerea:
        pass

    @abstractmethod
    async def reprocess(self, document_id: str):
        pass