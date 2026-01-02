from abc import ABC, abstractmethod
from typing import List

from app.modules.catalog.domain.catalogo import Catalogo


class CatalogoRepository(ABC):

    @abstractmethod
    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> List[Catalogo]:
        pass