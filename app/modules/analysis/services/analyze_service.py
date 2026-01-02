from abc import ABC, abstractmethod
from typing import Any, Dict, List
from fastapi import UploadFile

from app.modules.analysis.services.document_service import DocumentService

class AnalyzeService(ABC):

    @abstractmethod
    async def upload(self, t: List[UploadFile]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def upload_stream(self, files_data: List[Dict[str, Any]], document_service: DocumentService):
        pass