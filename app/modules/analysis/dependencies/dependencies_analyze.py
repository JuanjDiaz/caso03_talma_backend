from functools import lru_cache
from app.modules.analysis.services.analyze_service import AnalyzeService
from app.modules.analysis.services.impl.analyze_service_impl import AnalyzeServiceImpl
from app.modules.integration.extraction_engine import ExtractionEngine
from app.modules.integration.impl.extraction_engine_impl import ExtractionEngineImpl

@lru_cache()
def get_extraction_engine() -> ExtractionEngine:
    return ExtractionEngineImpl()


@lru_cache()
def get_analyze_service() -> AnalyzeService:
    engine = get_extraction_engine()
    return AnalyzeServiceImpl(extraction_engine=engine)



