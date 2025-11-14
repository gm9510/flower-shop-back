from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Esquema para Carrito
class CarritoBase(BaseModel):
    idEntidad: Optional[int] = None
    sessionToken: str


class CarritoCreate(CarritoBase):
    pass


class CarritoUpdate(CarritoBase):
    pass


class Carrito(CarritoBase):
    id: int
    registro: Optional[datetime] = None

    class Config:
        from_attributes = True