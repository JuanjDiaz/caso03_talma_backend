from app.configuration.repository.catalogo_repository import CatalogoRepository
from app.configuration.service.catalogo_service import CatalogoService
from typing import List
from utl.constantes import Catalogo

class CatalogoServiceImpl(CatalogoService):

    def __init__(self, catalogo_repository: CatalogoRepository):
        self.catalogo_repository = catalogo_repository

    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> List[Catalogo]:
        return await self.catalogo_repository.load_by_referencia_nombre(referenciaCodigo)

