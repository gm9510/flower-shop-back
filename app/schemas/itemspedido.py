from pydantic import BaseModel


class ItemsPedidoCreate(BaseModel):
    pedidoId: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float


class ItemsPedidoResponse(BaseModel):
    id: int
    pedidoId: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float

    class Config:
        from_attributes = True
