from pydantic import BaseModel
from typing import Optional
from datetime import date


class CuponCreate(BaseModel):
    codigo: str
    tipoDescuento: str  # 'porcentaje' o 'monto_fijo'
    valorDescuento: float
    validoDesde: Optional[date] = None
    validoHasta: Optional[date] = None
    limiteUso: Optional[int] = None


class CuponResponse(BaseModel):
    id: int
    codigo: str
    tipoDescuento: str
    valorDescuento: float
    validoDesde: Optional[date] = None
    validoHasta: Optional[date] = None
    limiteUso: Optional[int] = None

    class Config:
        from_attributes = True
