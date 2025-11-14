from pydantic import BaseModel
from typing import Optional


# Esquema para ProductoEnsamble
class ProductoEnsambleBase(BaseModel):
    idProductoPadre: int
    cantidad: float
    idProductoHijo: int


class ProductoEnsambleCreate(ProductoEnsambleBase):
    pass


class ProductoEnsambleUpdate(ProductoEnsambleBase):
    pass


class ProductoEnsamble(ProductoEnsambleBase):
    id: int

    class Config:
        from_attributes = True