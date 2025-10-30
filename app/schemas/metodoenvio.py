from pydantic import BaseModel
from typing import Optional


class MetodoEnvioCreate(BaseModel):
    nombre: str
    costo: float
    tiempoEstimadoEntrega: Optional[int] = None


class MetodoEnvioResponse(BaseModel):
    id: int
    nombre: str
    costo: float
    tiempoEstimadoEntrega: Optional[int] = None

    class Config:
        from_attributes = True
