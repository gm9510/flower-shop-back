from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Esquema para Compra
class CompraBase(BaseModel):
    idEntidad: int
    factura: Optional[str] = None
    subTotal: float
    descuento: Optional[float] = 0.0
    total: float
    saldo: Optional[float] = 0.0
    metodoPago: Optional[str] = "DE CONTADO"
    fechaLimite: Optional[datetime] = None
    efectivo: Optional[float] = None
    transferencia: Optional[float] = None
    observacion: Optional[str] = None
    usuario: Optional[str] = None
    registro: datetime


class CompraCreate(CompraBase):
    pass


class CompraUpdate(CompraBase):
    pass


class Compra(CompraBase):
    id: int

    class Config:
        from_attributes = True