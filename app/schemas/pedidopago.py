from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoPagoEnum(str, Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"


class OpcionPagoEnum(str, Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"


# Esquema para PedidoPago
class PedidoPagoBase(BaseModel):
    idPedido: int
    pasarelaPagoId: str
    monto: float
    estadoPago: Optional[EstadoPagoEnum] = EstadoPagoEnum.PENDIENTE
    opcionPago: Optional[OpcionPagoEnum] = OpcionPagoEnum.EFECTIVO
    idTransaccion: Optional[str] = None
    usuario: Optional[str] = None


class PedidoPagoCreate(PedidoPagoBase):
    pass


class PedidoPagoUpdate(PedidoPagoBase):
    pass


class PedidoPago(PedidoPagoBase):
    id: int
    registro: Optional[datetime] = None

    class Config:
        from_attributes = True