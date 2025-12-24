from abc import ABC, abstractmethod
from typing import List

from app.configuration.domain.catalogo import Catalogo


class CatalogoRepository(ABC):

    @abstractmethod
    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> List[Catalogo]:
        pass