from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PedidosCreate(BaseModel):
    clienteId: int
    montoTotal: float
    estadoPedido: str = 'pendiente'
    estadoPago: str = 'pendiente'
    metodoPago: Optional[str] = None
    direccionEnvio: Optional[str] = None
    cuponId: Optional[int] = None
    metodoEnvioId: Optional[int] = None


class PedidosResponse(BaseModel):
    id: int
    clienteId: int
    montoTotal: float
    estadoPedido: str
    estadoPago: str
    metodoPago: Optional[str] = None
    direccionEnvio: Optional[str] = None
    cuponId: Optional[int] = None
    metodoEnvioId: Optional[int] = None
    creadoEn: datetime

    class Config:
        from_attributes = True
