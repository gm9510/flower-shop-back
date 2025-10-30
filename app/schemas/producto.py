from pydantic import BaseModel
from typing import Optional


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoriaId: Optional[int] = None
    imagenUrl: Optional[str] = None


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoriaId: Optional[int] = None
    imagenUrl: Optional[str] = None

    class Config:
        from_attributes = True
