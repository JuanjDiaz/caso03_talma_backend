from typing import Type, Any
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta
from uuid import UUID
from sqlalchemy import inspect

class Mapper:
    @staticmethod
    def to_dto(entity: Any, dto_class: Type[BaseModel]):
        data = {}
        for field_name in dto_class.model_fields.keys():
            value = None
            if hasattr(entity, field_name):
                 value = getattr(entity, field_name)
            else:
                snake_name = Mapper._to_snake_case(field_name)
                if hasattr(entity, snake_name):
                    value = getattr(entity, snake_name)
            
            if value is not None:
                if isinstance(value, UUID):
                    data[field_name] = str(value)
                else:
                    data[field_name] = value
        
        return dto_class(**data)

    @staticmethod
    def _to_snake_case(name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def to_entity(dto: BaseModel, entity_class: Type[DeclarativeMeta]):
        # 1. Obtener columnas y relaciones
        valid_fields = {c.name for c in entity_class.__table__.columns}
        # Obtener nombres de las relaciones definidas en el modelo (ej: 'intervinientes')
        relationships = getattr(inspect(entity_class), "relationships", {}).keys()
        
        data = dto.model_dump()
        mapped_data = {}
        
        for k, v in data.items():
            if v is None:
                continue
                
            # Determinar el nombre en snake_case para comparar
            target_key = k if k in valid_fields or k in relationships else Mapper._to_snake_case(k)

            # CASO A: Es una columna normal
            if target_key in valid_fields:
                mapped_data[target_key] = v
            
            # CASO B: Es una RELACIÓN (Como intervinientes o confianzas)
            elif target_key in relationships:
                rel_property = inspect(entity_class).relationships[target_key]
                related_class = rel_property.mapper.class_
                
                if isinstance(v, list):
                    # Convertir cada DTO de la lista en una entidad
                    mapped_data[target_key] = [Mapper.to_entity_from_dict(item, related_class) for item in v]
                elif isinstance(v, dict):
                    mapped_data[target_key] = Mapper.to_entity_from_dict(v, related_class)

        return entity_class(**mapped_data)

    @staticmethod
    def to_entity_from_dict(data: dict, entity_class: Type[DeclarativeMeta]):
        valid_fields = {c.name for c in entity_class.__table__.columns}
        mapped_data = {}
        
        # 1. Mapeo estándar de campos (nombre, direccion, etc.)
        for k, v in data.items():
            snake_k = Mapper._to_snake_case(k)
            if snake_k in valid_fields:
                mapped_data[snake_k] = v
        
        # 2. TRADUCCIÓN CRÍTICA: tipo_codigo -> rol_codigo
        # El LLM envía 'tipoCodigo', el DTO lo recibe, pero la DB usa 'rol_codigo'
        tipo_envio = data.get("tipoCodigo") or data.get("tipo_codigo")
        
        if tipo_envio == "TPIN001":
            mapped_data["rol_codigo"] = "REMITENTE"
        elif tipo_envio == "TPIN002":
            mapped_data["rol_codigo"] = "CONSIGNATARIO"
        # Si por alguna razón ya viene como rolCodigo en el dict
        elif data.get("rolCodigo"):
            mapped_data["rol_codigo"] = data.get("rolCodigo")

        # 3. Auditoría y Estado Activo
        if "es_version_activa" in valid_fields:
            mapped_data["es_version_activa"] = True
        if "habilitado" in valid_fields:
            mapped_data["habilitado"] = True
            
        return entity_class(**mapped_data)
