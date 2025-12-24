from fastapi import APIRouter, Depends
from app.security.dependencies.dependencies_usuario import get_usuario_facade
from app.security.facade.usuario_facade import UsuarioFacade
from dto.universal_dto import BaseOperacionResponse
from dto.usuario_dtos import UsuarioRequest


router = APIRouter()

@router.post("/saveOrUpdate", response_model=BaseOperacionResponse)
async def saveOrUpdate( request: UsuarioRequest, usuario_facade: UsuarioFacade = Depends(get_usuario_facade)) -> BaseOperacionResponse:
    return await usuario_facade.saveOrUpdate(request)