from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# Enumeraciones
class MetodoPagoEnum(str, Enum):
    contado = "DE CONTADO"
    credito = "A CREDITO"


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
    completado = "completado"


class OpcionPagoEnum(str, Enum):
    efectivo = "efectivo"
    transferencia = "trasnferencia"


class TipoDescuentoEnum(str, Enum):
    porcentaje = "porcentaje"
    monto_fijo = "monto_fijo"


# Esquema para Entidad
class EntidadBase(BaseModel):
    nit: str
    dv: Optional[int] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    estado: Optional[bool] = None
    direccion: Optional[str] = None


class EntidadCreate(EntidadBase):
    pass


class EntidadUpdate(EntidadBase):
    pass


class Entidad(EntidadBase):
    id: int

    class Config:
        from_attributes = True