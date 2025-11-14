from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoPagoEnum(str, Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    fallido = "fallido"
    reembolsado = "reembolsado"
    completado = "completado"


class OpcionPagoEnum(str, Enum):
    efectivo = "efectivo"
    transferencia = "trasnferencia"


# Esquema para PedidoPago
class PedidoPagoBase(BaseModel):
    idPedido: int
    pasarelaPagoId: str
    monto: float
    estadoPago: Optional[EstadoPagoEnum] = EstadoPagoEnum.pendiente
    opcionPago: Optional[OpcionPagoEnum] = OpcionPagoEnum.efectivo
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