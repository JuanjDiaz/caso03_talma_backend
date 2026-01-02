from typing import Type, Any
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta
from uuid import UUID

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
        valid_fields = {c.name for c in entity_class.__table__.columns}
        data = dto.model_dump()
        mapped_data = {}
        
        for k, v in data.items():
            if v is None:
                continue
                
            if k in valid_fields:
                mapped_data[k] = v
                continue
            
            snake_k = Mapper._to_snake_case(k)
            if snake_k in valid_fields:
                mapped_data[snake_k] = v
        
        return entity_class(**mapped_data)
