from typing import Any
from app.modules.analysis.domain.confianza_extraccion import ConfianzaExtraccion
from app.modules.analysis.repository.confianza_extraccion_repository import ConfianzaExtraccionRepository
from app.modules.analysis.services.confianza_extraccion_service import ConfianzaExtraccionService
from app.config.mapper import Mapper
from app.core.service.service_base import ServiceBase
from app.dto.guia_aerea_dtos import GuiaAereaRequest
from app.utils.date_util import DateUtil
from app.utils.constantes import Constantes

class ConfianzaExtraccionServiceImpl(ConfianzaExtraccionService, ServiceBase):

    def __init__(self, confianza_extraccion_repository: ConfianzaExtraccionRepository):
        self.confianza_extraccion_repository = confianza_extraccion_repository


    