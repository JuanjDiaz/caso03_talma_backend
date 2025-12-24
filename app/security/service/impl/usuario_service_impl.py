from app.security.domain import Usuario
from app.security.repository.usuario_repository import UsuarioRepository
from app.security.service.usuario_service import UsuarioService
from config.mapper import Mapper
from dto.universal_dto import BaseOperacionResponse
from dto.usuario_dtos import UsuarioRequest
from utl.generic_util import GenericUtil


class UsuarioServiceImpl(UsuarioService):

    def __init__(self, usuario_repository: UsuarioRepository, modelMapper: Mapper):
        self.usuario_repository = usuario_repository
        self.modelMapper = modelMapper

    async def saveOrUpdate(self, t: UsuarioRequest) -> None:

        if GenericUtil.no_es_nulo(t, "usuarioId"):
            usuario = await self.usuario_repository.find_by_id(t.usuarioId)

            if usuario is None:
                raise NotFoundException("Usuario no existe")

            usuario = self.modelMapper.to_entity(t, Usuario)
            await self.usuario_repository.update(usuario)

     
        else:
            usuario = self.modelMapper.to_entity(t, Usuario)
            usuario.usuario = t.primerNombre + t.apellidoPaterno + GenericUtil.generate_unique_code_8()
            await self.usuario_repository.save(usuario)
            