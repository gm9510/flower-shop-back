from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoPedidoEnum(str, Enum):
    pendiente = "pendiente"
    procesando = "procesando"
    enviado = "enviado"
    entregado = "entregado"
    cancelado = "cancelado"


class EstadoPagoEnum(str, Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    fallido = "fallido"
    reembolsado = "reembolsado"


# Esquema para Pedido
class PedidoBase(BaseModel):
    numeroFactura: Optional[int] = None
    idEntidad: int
    subTotal: float
    descuento: Optional[float] = None
    montoTotal: float
    saldo: Optional[float] = None
    estadoPedido: Optional[EstadoPedidoEnum] = EstadoPedidoEnum.pendiente
    estadoPago: Optional[EstadoPagoEnum] = EstadoPagoEnum.pendiente
    metodoPago: Optional[str] = "DE CONTADO"
    fechaEntrega: datetime = None
    direccionEnvio: Optional[str] = None
    idCupon: Optional[int] = None
    idEnvio: Optional[int] = None
    efectivo: Optional[int] = None
    transferencia: Optional[int] = None
    usuario: Optional[str] = None
    registro: Optional[datetime] = None


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(PedidoBase):
    pass


class Pedido(PedidoBase):
    id: int

    class Config:
        from_attributes = True