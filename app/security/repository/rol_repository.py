from abc import abstractmethod
from typing import List
from app.integration.base_repository import BaseRepository
from app.security.domain import Rol


class RolRepository(BaseRepository[Rol]):
    
    @abstractmethod
    async def load() -> List[Rol]:
        pass