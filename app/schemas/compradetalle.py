from pydantic import BaseModel
from typing import Optional


# Esquema para CompraDetalle
class CompraDetalleBase(BaseModel):
    idCompra: int
    idProducto: int
    cantidad: int
    costo: float
    iva: Optional[int] = 0
    costoIva: float
    totalUnitario: Optional[float] = None
    precioVenta: Optional[float] = None


class CompraDetalleCreate(CompraDetalleBase):
    pass


class CompraDetalleUpdate(CompraDetalleBase):
    pass


class CompraDetalle(CompraDetalleBase):
    id: int

    class Config:
        from_attributes = True