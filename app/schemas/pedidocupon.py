from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoDescuentoEnum(str, Enum):
    PORCENTAJE = "porcentaje"
    MONTO_FIJO = "monto_fijo"


# Esquema para PedidoCupon
class PedidoCuponBase(BaseModel):
    codigo: str
    tipoDescuento: TipoDescuentoEnum
    valorDescuento: float
    validoDesde: Optional[datetime] = None
    validoHasta: Optional[datetime] = None
    limiteUso: Optional[int] = None


class PedidoCuponCreate(PedidoCuponBase):
    pass


class PedidoCuponUpdate(PedidoCuponBase):
    pass


class PedidoCupon(PedidoCuponBase):
    id: int

    class Config:
        from_attributes = True