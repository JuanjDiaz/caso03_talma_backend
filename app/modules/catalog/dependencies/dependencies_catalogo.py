from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.catalog.facade.impl.comun_facade_impl import ComunFacadeImpl
from app.modules.catalog.repository.impl.catalogo_repository_impl import CatalogoRepositoryImpl
from app.modules.catalog.service.impl.catalogo_service_impl import CatalogoServiceImpl
from app.modules.analysis.facade.document_facade import DocumentFacade
from app.modules.analysis.facade.impl.document_facade_impl import DocumentFacadeImpl
from app.modules.analysis.repository.impl.document_repository_impl import DocumentRepositoryImpl
from app.modules.analysis.services.impl.document_service_impl import DocumentServiceImpl
from app.config.database_config import get_db
from app.modules.security.dependencies.dependencies_rol import get_rol_service

def get_catalogo_repository(db: AsyncSession = Depends(get_db)):
    return CatalogoRepositoryImpl(db)

def get_catalogo_service(repository = Depends(get_catalogo_repository)):
    return CatalogoServiceImpl(repository)

def get_comun_facade(service = Depends(get_catalogo_service), rol_service = Depends(get_rol_service)):
    return ComunFacadeImpl(service, rol_service)
