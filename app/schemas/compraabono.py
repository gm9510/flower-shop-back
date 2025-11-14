from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class OpcionPagoEnum(str, Enum):
    efectivo = "efectivo"
    transferencia = "trasnferencia"


# Esquema para CompraAbono
class CompraAbonoBase(BaseModel):
    idCompra: int
    valor: float
    opcionPago: Optional[OpcionPagoEnum] = OpcionPagoEnum.efectivo
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