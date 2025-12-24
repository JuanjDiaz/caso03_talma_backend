from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.configuration.facade.impl.comun_facade_impl import ComunFacadeImpl
from app.configuration.repository.impl.catalogo_repository_impl import CatalogoRepositoryImpl
from app.configuration.service.impl.catalogo_service_impl import CatalogoServiceImpl
from app.core.facade.document_facade import DocumentFacade
from app.core.facade.impl.document_facade_impl import DocumentFacadeImpl
from app.core.repository.impl.document_repository_impl import DocumentRepositoryImpl
from app.core.services.impl.document_service_impl import DocumentServiceImpl
from config.database_config import get_db
from app.security.dependencies.dependencies_rol import get_rol_service

def get_catalogo_repository(db: AsyncSession = Depends(get_db)):
    return CatalogoRepositoryImpl(db)

def get_catalogo_service(repository = Depends(get_catalogo_repository)):
    return CatalogoServiceImpl(repository)

def get_comun_facade(service = Depends(get_catalogo_service), rol_service = Depends(get_rol_service)):
    return ComunFacadeImpl(service, rol_service)
