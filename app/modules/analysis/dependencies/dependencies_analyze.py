from functools import lru_cache
from app.modules.analysis.services.analyze_service import AnalyzeService
from app.modules.analysis.services.impl.analyze_service_impl import AnalyzeServiceImpl
from app.modules.analysis.services.document_service import DocumentService
from app.modules.analysis.dependencies.dependencies_documento import get_document_service
from app.modules.integration.extraction_engine import ExtractionEngine
from app.modules.integration.impl.extraction_engine_impl import ExtractionEngineImpl
from fastapi import Depends

@lru_cache()
def get_extraction_engine() -> ExtractionEngine:
    return ExtractionEngineImpl()


def get_analyze_service(engine: ExtractionEngine = Depends(get_extraction_engine)) -> AnalyzeService:
    return AnalyzeServiceImpl(extraction_engine=engine)



