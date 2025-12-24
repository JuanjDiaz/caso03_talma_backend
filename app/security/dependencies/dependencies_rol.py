from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.security.repository.impl.rol_repository_impl import RolRepositoryImpl
from app.security.service.impl.rol_service_impl import RolServiceImpl
from config.database_config import get_db

def get_rol_repository(db: AsyncSession = Depends(get_db)):
    return RolRepositoryImpl(db)

def get_rol_service(repository = Depends(get_rol_repository)):
    return RolServiceImpl(repository)