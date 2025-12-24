from typing import List
from sqlalchemy import select
from app.configuration.repository.catalogo_repository import CatalogoRepository
from app.configuration.domain.catalogo import Catalogo
from sqlalchemy.ext.asyncio import AsyncSession
from app.integration.impl.base_repository_impl import BaseRepositoryImpl

class CatalogoRepositoryImpl(BaseRepositoryImpl[Catalogo], CatalogoRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(Catalogo, db)

    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> List[Catalogo]:
        query = (
            select(Catalogo)
            .where(Catalogo.referencia_codigo == referenciaCodigo)
            .where(Catalogo.habilitado == True)
            .order_by(Catalogo.nombre.asc())
        )
        result = await self.db.execute(query)
        return result.scalars().all()