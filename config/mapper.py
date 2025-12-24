from typing import Type, Any
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta

class Mapper:
    @staticmethod
    def to_dto(entity: Any, dto_class: Type[BaseModel]):
        return dto_class.from_orm(entity)

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
                
            # 1. Exact match
            if k in valid_fields:
                mapped_data[k] = v
                continue
            
            # 2. Snake case match
            snake_k = Mapper._to_snake_case(k)
            if snake_k in valid_fields:
                mapped_data[snake_k] = v
        
        return entity_class(**mapped_data)
