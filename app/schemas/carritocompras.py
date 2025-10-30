from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CarritoComprasCreate(BaseModel):
    clienteId: int
    productoId: int
    cantidad: int = 1


class CarritoComprasResponse(BaseModel):
    id: int
    clienteId: int
    productoId: int
    cantidad: int
    agregadoEn: datetime

    class Config:
        from_attributes = True
