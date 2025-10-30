from pydantic import BaseModel
from typing import Optional


class EntidadCreate(BaseModel):
    tipoEntidad: str  # 'cliente' o 'proveedor'
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contacto: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None


class EntidadResponse(BaseModel):
    id: int
    tipoEntidad: str
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contacto: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

    class Config:
        from_attributes = True
