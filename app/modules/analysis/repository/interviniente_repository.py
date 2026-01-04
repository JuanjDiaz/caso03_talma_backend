from typing import Optional
from app.modules.analysis.domain.interviniente import Interviniente
from app.modules.integration.impl.base_repository_impl import BaseRepositoryImpl
from abc import abstractmethod

class IntervinienteRepository(BaseRepositoryImpl[Interviniente]):
    
    @abstractmethod
    async def find_by_documento_tipo(self, numero_documento: str, tipo_codigo: str) -> Optional[Interviniente]:
        pass