from pydantic import BaseModel
from typing import Optional


class SedeCreate(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None


class SedeResponse(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: Optional[str] = None

    class Config:
        from_attributes = True
