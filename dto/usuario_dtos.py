from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

from dto.universal_dto import ComboBaseResponse


class UsuarioRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    usuarioId: Optional[str] = None
    rolId: Optional[str] = None
    primerNombre: Optional[str] = None
    segundoNombre: Optional[str] = None
    apellidoPaterno: Optional[str] = None
    apellidoMaterno: Optional[str] = None
    correo: Optional[EmailStr] = None
    celular: Optional[str] = Field(None, min_length=9, max_length=15)
    tipoDocumentoCodigo: Optional[str] = None
    documento: Optional[str] = None


class UsuarioComboResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tipoDocumento: Optional[ComboBaseResponse] = None
    rol: Optional[ComboBaseResponse] = None

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    usuarioId: Optional[str] = None
    rolId: Optional[str] = None
    primerNombre: Optional[str] = None
    segundoNombre: Optional[str] = None
    apellidoPaterno: Optional[str] = None
    apellidoMaterno: Optional[str] = None
    correo: Optional[EmailStr] = None
    celular: Optional[str] = Field(None, min_length=9, max_length=15)
    tipoDocumentoCodigo: Optional[str] = None
    documento: Optional[str] = None
    combo: Optional[UsuarioComboResponse] = None
