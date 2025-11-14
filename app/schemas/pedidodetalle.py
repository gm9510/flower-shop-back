from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Esquema para PedidoDetalle
class PedidoDetalleBase(BaseModel):
    idPedido: int
    idProducto: int
    cantidad: int
    precioUnitario: float
    resigstro: Optional[datetime] = None  # Nota: hay un error tipográfico en el esquema original


class PedidoDetalleCreate(PedidoDetalleBase):
    pass


class PedidoDetalleUpdate(PedidoDetalleBase):
    pass


class PedidoDetalle(PedidoDetalleBase):
    id: int

    class Config:
        from_attributes = True