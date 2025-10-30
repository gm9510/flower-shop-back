from pydantic import BaseModel
from typing import Optional


class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

    class Config:
        from_attributes = True
