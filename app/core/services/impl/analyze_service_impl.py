import base64
import asyncio
import logging
from io import BytesIO
import fitz
from typing import Any, Dict, List
from fastapi import UploadFile

from app.core.services.analyze_service import AnalyzeService
from app.integration.extraction_engine import ExtractionEngine
from core.exceptions import AppBaseException
from utl.file_util import FileUtil

logger = logging.getLogger(__name__)

def process_file_content(content: bytes, filename: str) -> List[str]:
    """
    CPU-bound task to convert PDF/Images to base64.
    Executed in a thread pool to avoid blocking the main event loop.
    """
    base64_results = []

    if FileUtil.is_valid_pdf(content):
        try:
            doc = fitz.open(stream=BytesIO(content), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("jpeg")
                base64_results.append(base64.b64encode(img_bytes).decode("utf-8"))
            doc.close()
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {e}", exc_info=True)
            return []

    elif FileUtil.is_valid_image(content):
        base64_results.append(base64.b64encode(content).decode("utf-8"))

    return base64_results

class AnalyzeServiceImpl(AnalyzeService):

    def __init__(self, extraction_engine: ExtractionEngine):
        self.extraction_engine = extraction_engine

    async def upload(self, t: List[UploadFile]) -> List[Dict[str, Any]]:
        results = []
        loop = asyncio.get_running_loop()

        for file in t:
            content = await file.read()
            # Offload CPU-bound work to thread pool
            pages = await loop.run_in_executor(None, process_file_content, content, file.filename)

            if not pages:
                logger.warning(f"File {file.filename} is corrupt or invalid.")
                raise AppBaseException(
                    message=f"El archivo {file.filename} está corrupto, vacío o tiene un formato no soportado."
                )
            
            file_extracted_data = []
            for idx, page_img in enumerate(pages):
                data = await self.extraction_engine.extract_data_from_image(page_img)
                file_extracted_data.append({
                    "page": idx + 1,
                    "content": data
                })

            results.append({
                "filename": file.filename,
                "total_pages": len(pages),
                "data": file_extracted_data
            })

        return results


    async def upload_stream(self, files_data: List[Dict[str, Any]]):
        all_pages = []
        total_files = len(files_data)
        loop = asyncio.get_running_loop()

        for idx, file_data in enumerate(files_data):
            filename = file_data.get("filename")
            content = file_data.get("content")
            
            yield f"data: Procesando archivo {idx + 1}/{total_files}: {filename}...\n\n"

            # Offload CPU-bound work to thread pool
            try:
                pages = await loop.run_in_executor(None, process_file_content, content, filename)
            except Exception as e:
                logger.error(f"Error executing process_file_content for {filename}: {e}", exc_info=True)
                pages = []

            if not pages:
                logger.warning(f"File {filename} yielded no pages.")
                yield f"data: [ERROR] Archivo {filename} inválido o vacío\n\n"
                continue

            all_pages.extend(pages)

        if not all_pages:
             yield "data: [ERROR] No se encontraron imágenes válidas para analizar.\n\n"
             return

        yield f"data: Iniciando análisis con IA de {len(all_pages)} páginas en total...\n\n"

        async for token in self.extraction_engine.extract_stream(all_pages):
            yield f"data: {token}\n\n"

        yield "data: [OK] Análisis completado.\n\n"
