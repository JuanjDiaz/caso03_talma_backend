from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UsuarioRequest(BaseModel):
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

