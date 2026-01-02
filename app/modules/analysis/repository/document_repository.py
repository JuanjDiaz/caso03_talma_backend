from abc import  abstractmethod
from typing import Optional
from app.modules.integration.base_repository import BaseRepository
from app.modules.analysis.domain.guia_aerea import GuiaAerea

class DocumentRepository(BaseRepository[GuiaAerea]):
    
    @abstractmethod
    async def find_by_numero(self, numero: str, exclude_id: Optional[str] = None) -> Optional[GuiaAerea]:
        pass

    @abstractmethod
    async def get_by_id_with_relations(self, id: str) -> Optional[GuiaAerea]:
        pass

    