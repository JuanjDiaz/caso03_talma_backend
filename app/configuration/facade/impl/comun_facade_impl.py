import logging
from app.configuration.facade.comun_facade import ComunFacade
from app.configuration.service.catalogo_service import CatalogoService
from dto.universal_dto import ComboBaseResponse, ComboResponse



from app.security.service.rol_service import RolService

class ComunFacadeImpl(ComunFacade):

    def __init__(self, catalogo_service: CatalogoService, rol_service: RolService):
        self.catalogo_service = catalogo_service
        self.rol_service = rol_service

    async def load_by_referencia_nombre(self, referenciaCodigo: str) -> ComboBaseResponse:
        collections = []
        catalogos = await self.catalogo_service.load_by_referencia_nombre(referenciaCodigo)
        for tt in catalogos:
            collections.append(ComboResponse(id=tt.catalogo_id, codigo=tt.codigo, nombre=tt.nombre))
        
        return ComboBaseResponse(list=collections, size=len(collections))

    async def load_rol(self) -> ComboBaseResponse:
        collections = []
        roles = await self.rol_service.load()
        for tt in roles:
            collections.append(ComboResponse(id=tt.rol_id, codigo=tt.codigo, nombre=tt.nombre))
        
        return ComboBaseResponse(list=collections, size=len(collections))
    
