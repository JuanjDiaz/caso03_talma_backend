from app.modules.analysis.domain.confianza_extraccion import ConfianzaExtraccion
from app.modules.analysis.repository.confianza_extraccion_repository import ConfianzaExtraccionRepository
from app.modules.integration.impl.base_repository_impl import BaseRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession

class ConfianzaExtraccionRepositoryImpl(BaseRepositoryImpl[ConfianzaExtraccion], ConfianzaExtraccionRepository):
    
    def __init__(self, db: AsyncSession):
        super().__init__(ConfianzaExtraccion, db)

    
    