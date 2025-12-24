from app.security.facade.usuario_facade import UsuarioFacade
from app.security.service.usuario_service import UsuarioService
from dto.universal_dto import BaseOperacionResponse
from dto.usuario_dtos import UsuarioRequest


class UsuarioFacadeImpl(UsuarioFacade):

    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service
    
    async def saveOrUpdate(self, t: UsuarioRequest) -> BaseOperacionResponse:
        await self.usuario_service.saveOrUpdate(t)
        return BaseOperacionResponse(codigo="200", mensaje="Documentos guardados correctamente")
