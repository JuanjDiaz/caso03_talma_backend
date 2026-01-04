from abc import abstractmethod
from typing import Any, Optional
from app.modules.analysis.domain.guia_aerea_data_grid import GuiaAereaDataGrid
from app.modules.integration.base_repository import BaseRepository


class GuiaAereaFiltroRepository(BaseRepository[GuiaAereaDataGrid]):
    
    @abstractmethod
    async def find_data_grid(self, filters: list, start: int, limit: int, sort: Optional[str] = None) -> tuple[Any, int]:
        pass