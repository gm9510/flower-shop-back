from pydantic import BaseModel
from typing import Optional


# Esquema para Inventario
class InventarioBase(BaseModel):
    idProducto: Optional[int] = None
    stock: Optional[float] = 0.0


class InventarioCreate(InventarioBase):
    pass


class InventarioUpdate(InventarioBase):
    pass


class Inventario(InventarioBase):
    id: int

    class Config:
        from_attributes = True