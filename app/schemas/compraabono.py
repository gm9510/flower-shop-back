from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class OpcionPagoEnum(str, Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"


# Esquema para CompraAbono
class CompraAbonoBase(BaseModel):
    idCompra: int
    valor: float
    opcionPago: Optional[OpcionPagoEnum] = OpcionPagoEnum.EFECTIVO
    registro: datetime
    usuario: Optional[str] = None


class CompraAbonoCreate(CompraAbonoBase):
    pass


class CompraAbonoUpdate(CompraAbonoBase):
    pass


class CompraAbono(CompraAbonoBase):
    id: int

    class Config:
        from_attributes = True