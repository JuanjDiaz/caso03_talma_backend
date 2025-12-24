
from abc import ABC, abstractmethod
from typing import List
from utl.constantes import Catalogo



class CatalogoService(ABC):

    @abstractmethod
    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> List[Catalogo]:
        pass

