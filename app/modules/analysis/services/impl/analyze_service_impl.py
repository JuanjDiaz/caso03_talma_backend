import base64
import json
import asyncio
import logging
from io import BytesIO
import openpyxl
import fitz
from typing import Any, Dict, List, Tuple
from fastapi import UploadFile

from app.modules.analysis.services.analyze_service import AnalyzeService
from app.modules.integration.extraction_engine import ExtractionEngine
from app.core.exceptions import AppBaseException
from app.utils.file_util import FileUtil

logger = logging.getLogger(__name__)

def process_file_content(content: bytes, filename: str) -> Tuple[List[str], str]:
    """
    CPU-bound task to convert PDF/Images to base64 OR Extract text from Excel.
    Executed in a thread pool.
    Returns: (list_of_base64_images, extracted_text_string)
    """
    base64_results = []
    text_result = ""

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
            return [], ""

    elif FileUtil.is_valid_image(content):
        base64_results.append(base64.b64encode(content).decode("utf-8"))
    
    # Check for Excel
    elif filename.lower().endswith(('.xlsx', '.xlsm')):
        try:
            wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
            text_parts = []
            for sheet in wb.worksheets:
                text_parts.append(f"--- HOJA: {sheet.title} ---")
                for row in sheet.iter_rows(values_only=True):
                    # Convert row to CSV-like string, filtering None
                    row_str = ",".join([str(c) for c in row if c is not None])
                    if row_str.strip():
                        text_parts.append(row_str)
            text_result = "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error processing Excel {filename}: {e}", exc_info=True)
            return [], ""

    return base64_results, text_result

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
        all_docs_tasks = []
        total_files = len(files_data)
        
        # 1. Prepare all documents and calculate global indices
        current_global_page_index = 1
        for idx, file_data in enumerate(files_data):
            filename = file_data.get("filename")
            content = file_data.get("content")
            
            yield self._build_sse_event({"thinking": f"Preparando archivo {idx + 1}/{total_files}: {filename}...\n"})
            
            # Special case for Excel - keep our existing logic
            if filename.lower().endswith(('.xlsx', '.xlsm')):
                 loop = asyncio.get_running_loop()
                 _, excel_text = await loop.run_in_executor(None, process_file_content, content, filename)
                 if excel_text:
                      text_b64 = base64.b64encode(excel_text.encode('utf-8')).decode('utf-8')
                      task = self.extraction_engine.extract_single_document(
                          text_b64, 
                          "text/plain", 
                          1,
                          current_global_page_index
                      )
                      all_docs_tasks.append((task, filename, 1))
                      current_global_page_index += 1
                      continue

            # Standard case (PDF/Image) using demo's approach
            doc_prep = self.prepare_document_for_llm(content, filename)
            
            if not doc_prep:
                 yield self._build_sse_event({"thinking": f"[WARN] Archivo {filename} no soportado o vacío\n"})
                 continue

            page_count = doc_prep["page_count"]
            start_index = current_global_page_index
            
            # Schedule task for the entire document, passing page info
            task = self.extraction_engine.extract_single_document(
                doc_prep["base64"], 
                doc_prep["mime_type"], 
                page_count,
                start_index
            )
            all_docs_tasks.append((task, filename, page_count))
            
            # Increment global index for next file
            current_global_page_index += page_count
            logger.info(f"Added task for {filename} with {page_count} pages. Current global index: {current_global_page_index}")

        if not all_docs_tasks:
             logger.warning("No tasks were created for analysis.")
             yield self._build_sse_event({"thinking": "[ERROR] No se encontraron documentos válidos.\n"})
             return

        total_files_to_process = len(all_docs_tasks)
        yield self._build_sse_event({"thinking": f"Analizando {total_files_to_process} archivos en paralelo...\n"})

        # 2. Run in parallel
        try:
            completed_files_count = 0
            documents = []

            # Use demo's wrapper approach or similar to map results back to metadata
            # I'll use a safer task wrapping
            async def wrap_task(coro, fname, p_count):
                try:
                    return await coro, fname, p_count
                except Exception as e:
                    return [{"error": str(e)}], fname, p_count

            running_tasks = [wrap_task(t[0], t[1], t[2]) for t in all_docs_tasks]

            for future in asyncio.as_completed(running_tasks):
                results, fname, p_count = await future
                completed_files_count += 1
                
                yield self._build_sse_event({"thinking": f"Archivo '{fname}' ({p_count} pág) completado ({completed_files_count}/{total_files_to_process})\n"})
                
                if isinstance(results, list) and len(results) > 0 and results[0].get("error"):
                    err_msg = results[0].get("error")
                    logger.error(f"Error in task for {fname}: {err_msg}")
                    yield self._build_sse_event({"thinking": f"[ERROR] {fname}: {err_msg}\n"})
                else:
                    logger.info(f"Task for {fname} returned {len(results)} items.")
                    for page_result in results:
                        doc_obj = {
                            "document_index": page_result.get("document_index"),
                            "document_name": page_result.get("document_name") or f"{fname} - Pág {page_result.get('document_index')}",
                            "fileName": fname,
                            "fields": page_result.get("fields", {})
                        }
                        documents.append(doc_obj)

            # 3. Send Final JSON (sorted by document_index to keep order)
            documents.sort(key=lambda x: x.get("document_index", 0))
            logger.info(f"Finalizing analysis. Yielding {len(documents)} documents.")
            
            # Match demo exactly
            final_payload = json.dumps({"documents": documents})
            yield self._build_sse_event({"response": final_payload})
            
            yield self._build_sse_event({"thinking": f"Análisis finalizado exitosamente. {len(documents)} documentos detectados."})

        except Exception as e:
            logger.error(f"Critical Error during parallel extraction: {e}", exc_info=True)
            yield self._build_sse_event({"error": f"Error crítico: {str(e)}"})
            return


    def _build_sse_event(self, data: Dict[str, Any]) -> str:
        return f"data: {json.dumps(data)}\n\n"

    def prepare_document_for_llm(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Returns base64, mime_type, and page_count for the document."""
        logger.info(f"Iniciando preparación de archivo: {filename} (Tamaño: {len(content)} bytes)")
        
        if FileUtil.is_valid_pdf(content):
            try:
                doc = fitz.open(stream=BytesIO(content), filetype="pdf")
                page_count = doc.page_count
                doc.close()
                logger.info(f"Archivo {filename} identificado como PDF con {page_count} páginas.")
                return {
                    "base64": base64.b64encode(content).decode("utf-8"),
                    "mime_type": "application/pdf",
                    "page_count": page_count
                }
            except Exception as e:
                logger.error(f"Error procesando PDF {filename}: {e}")
                
        if FileUtil.is_valid_image(content):
            mime_type = "image/jpeg"
            ext = filename.lower().split('.')[-1]
            if ext == "png":
                mime_type = "image/png"
            elif ext == "webp":
                mime_type = "image/webp"
            
            logger.info(f"Archivo {filename} identificado como IMAGEN con MIME: {mime_type}")
            return {
                "base64": base64.b64encode(content).decode("utf-8"),
                "mime_type": mime_type,
                "page_count": 1
            }
        
        logger.warning(f"Archivo {filename} no pudo ser identificado como PDF ni como Imagen.")
        return None
