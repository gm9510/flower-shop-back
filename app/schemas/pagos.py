from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PagosCreate(BaseModel):
    pedidoId: int
    pasarelaPagoId: str
    monto: float
    estadoPago: str = 'pendiente'
    metodoPago: Optional[str] = None
    transaccionId: Optional[str] = None


class PagosResponse(BaseModel):
    id: int
    pedidoId: int
    pasarelaPagoId: str
    monto: float
    estadoPago: str
    metodoPago: Optional[str] = None
    transaccionId: Optional[str] = None
    creadoEn: datetime

    class Config:
        from_attributes = True
