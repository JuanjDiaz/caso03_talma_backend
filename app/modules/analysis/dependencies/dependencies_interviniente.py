from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.analysis.repository.impl.interviniente_repository_impl import IntervinienteRepositoryImpl
from app.modules.analysis.services.impl.interviniente_service_impl import IntervinienteServiceImpl
from app.config.database_config import get_db

def get_interviniente_repository(db: AsyncSession = Depends(get_db)):
    return IntervinienteRepositoryImpl(db)

def get_interviniente_service(repository = Depends(get_interviniente_repository)):
    return IntervinienteServiceImpl(repository)


