import json
import asyncio
import base64
import logging
import google.generativeai as genai
from app.modules.integration.extraction_engine import ExtractionEngine
from app.config.config import settings

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.LLM_API_KEY)
# Debug key format (length and start/end)
key_len = len(settings.LLM_API_KEY) if settings.LLM_API_KEY else 0
masked_key = f"{settings.LLM_API_KEY[:3]}...{settings.LLM_API_KEY[-3:]}" if key_len > 6 else "SHORT_KEY"
logger.info(f"GenAI configured with key length: {key_len} ({masked_key})")

class ExtractionEngineImpl(ExtractionEngine):

    async def extract_single_document(self, base64_data: str, mime_type: str, page_count: int, start_index: int) -> list[dict]:
        model = genai.GenerativeModel(settings.LLM_MODEL_NAME)
        
        is_pdf = mime_type == "application/pdf"
        is_text = mime_type == "text/plain"

        # General instructions for the LLM
        system_instructions = """Eres un experto en extracción de datos (OCR) y análisis de documentos.
Tu objetivo es extraer TODA la información del documento adjunto de forma estructurada.

REGLAS DE ORO:
1. Si encuentras TABLAS, lístalas como un ARRAY de OBJETOS dentro de una clave en 'fields'.
   Ejemplo: "fields": { "Tabla_Actividades": [ {"Columna1": "Fila1_Val1", "Columna2": "Fila1_Val2"}, ... ] }
2. Si el texto es MANUSCRITO (a mano), haz tu mejor esfuerzo por transcribirlo fielmente.
3. NO inventes datos. Si algo es ilegible, usa null.
4. Mantén los nombres de campos en MAYÚSCULAS y descriptivos.
5. Devuelve SIEMPRE una lista (array) JSON."""

        if is_text:
            prompt = f"""{system_instructions}

Analiza este contenido de TEXTO (Excel/CSV).
Responde con un solo objeto en la lista.

Formato requerido:
[
  {{
    "document_index": {start_index},
    "document_name": "Datos de Excel/Texto",
    "fields": {{ ... }}
  }}
]"""

            try:
                decoded_text = base64.b64decode(base64_data).decode('utf-8')
                contents = [prompt, decoded_text]
            except:
                contents = [prompt, base64_data]

        elif is_pdf:
            prompt = f"""{system_instructions}

Analiza este documento PDF por completo ({page_count} páginas).
Debes devolver exactamente UNA LISTA con {page_count} objetos (uno por página).

Formato requerido:
[
  {{
    "document_index": {start_index}, 
    "document_name": "Nombre descriptivo de la página",
    "fields": {{ ... }}
  }},
  ... (exactamente {page_count} páginas)
]"""
            contents = [prompt, {"mime_type": mime_type, "data": base64_data}]
        else:
            # Images - specifically emphasize handwritten tables here
            prompt = f"""{system_instructions}

Analiza esta IMAGEN. Puede contener texto MANUSCRITO y TABLAS.
Es fundamental extraer las tablas correctamente como listas de objetos para que se visualicen bien.

Formato requerido:
[
  {{
    "document_index": {start_index},
    "document_name": "Análisis de Imagen",
    "fields": {{ ... }}
  }}
]"""
            contents = [prompt, {"mime_type": mime_type, "data": base64_data}]

        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"AI Call attempt {attempt+1} for index {start_index} (Mime: {mime_type}, Model: {settings.LLM_MODEL_NAME})")
                response = await model.generate_content_async(
                    contents,
                    generation_config={
                        "response_mime_type": "application/json"
                    }
                )
                
                if response.text:
                    text = response.text.strip()
                    logger.debug(f"AI Raw Response for {start_index}: {text[:300]}...")
                    
                    if text.startswith("```"):
                        lines = text.splitlines()
                        if lines[0].startswith("```"): lines = lines[1:]
                        if lines[-1].startswith("```"): lines = lines[:-1]
                        text = "\n".join(lines).strip()
                    
                    try:
                        result_data = json.loads(text)
                    except json.JSONDecodeError:
                        logger.error(f"JSON ERROR for index {start_index}: {text}")
                        return [{"document_index": start_index, "error": "LLM returned invalid JSON"}]

                    extracted_list = []
                    if isinstance(result_data, list):
                        extracted_list = result_data
                    elif isinstance(result_data, dict):
                        for key in ["documents", "results", "pages", "data"]:
                            if key in result_data and isinstance(result_data[key], list):
                                extracted_list = result_data[key]
                                break
                        if not extracted_list:
                            extracted_list = [result_data]
                    
                    for item in extracted_list:
                        if not isinstance(item, dict): continue
                        if "document_index" not in item: item["document_index"] = start_index
                        if "fields" not in item or not item["fields"]:
                            item["fields"] = {"INFO": "No se detectaron campos específicos"}
                    
                    return extracted_list
                else:
                    return [{"document_index": start_index, "error": "Empty AI response"}]

            except Exception as e:
                logger.error(f"AI Error for index {start_index}: {e}", exc_info=True)
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return [{"document_index": start_index, "error": str(e)}]
        
        return [{"document_index": start_index, "error": "Max retries exceeded"}]