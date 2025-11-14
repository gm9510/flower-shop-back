from pydantic import BaseModel
from typing import Optional


# Esquema para CarritoDetalle
class CarritoDetalleBase(BaseModel):
    idCarrito: int
    idProducto: int
    cantidad: int
    precioUnitario: float


class CarritoDetalleCreate(CarritoDetalleBase):
    pass


class CarritoDetalleUpdate(CarritoDetalleBase):
    pass


class CarritoDetalle(CarritoDetalleBase):
    id: int

    class Config:
        from_attributes = True