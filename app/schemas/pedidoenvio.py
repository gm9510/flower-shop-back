from pydantic import BaseModel
from typing import Optional


# Esquema para PedidoEnvio
class PedidoEnvioBase(BaseModel):
    nombre: str
    costo: Optional[float] = 0.0
    tiempoEstimadoEntrega: Optional[int] = None


class PedidoEnvioCreate(PedidoEnvioBase):
    pass


class PedidoEnvioUpdate(PedidoEnvioBase):
    pass


class PedidoEnvio(PedidoEnvioBase):
    id: int

    class Config:
        from_attributes = True