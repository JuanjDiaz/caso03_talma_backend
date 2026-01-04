from abc import ABC, abstractmethod
from typing import List

from app.modules.security.domain import Rol


class RolService(ABC):

    @abstractmethod
    async def load() -> List[Rol]:
        pass