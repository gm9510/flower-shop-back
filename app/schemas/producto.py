from pydantic import BaseModel
from typing import Optional


# Esquema para Producto
class ProductoBase(BaseModel):
    nombre: Optional[str] = None
    precioVenta: Optional[int] = None
    tipo: Optional[str] = 'SIMPLE'
    categoria: str
    codbarra: Optional[str] = None
    estado: Optional[str] = None
    descripcion: Optional[str] = None
    imagenUrl: Optional[str] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True