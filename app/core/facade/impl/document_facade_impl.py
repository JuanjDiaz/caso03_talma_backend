import logging
from typing import List
from app.core.facade.document_facade import DocumentFacade
from app.core.services.document_service import DocumentService
from dto.document import DocumentRequest
from dto.universal_dto import BaseOperacionResponse

logger = logging.getLogger(__name__)

class DocumentFacadeImpl(DocumentFacade):

    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    async def save(self, t: List[DocumentRequest]) -> BaseOperacionResponse:
        try:
            for tt in t:
                await self.document_service.save(tt)
            return BaseOperacionResponse(codigo="200", mensaje="Documentos guardados correctamente")
        except Exception as e:
            logger.error(f"Error in facade save: {e}", exc_info=True)
            return BaseOperacionResponse(codigo="500", mensaje=f"Error al guardar documentos: {e}")

    async def get_all_documents(self, skip: int = 0, limit: int = 10):
        return await self.document_service.get_all_documents(skip, limit)