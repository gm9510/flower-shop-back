from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComprasCreate(BaseModel):
    idProveedor: int
    idSede: int
    total: float
    estadoCompra: str = 'pendiente'


class ComprasResponse(BaseModel):
    id: int
    idProveedor: int
    idSede: int
    total: float
    estadoCompra: str
    creadoEn: datetime

    class Config:
        from_attributes = True
