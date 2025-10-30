from pydantic import BaseModel


class DetallesCompraCreate(BaseModel):
    idCompra: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float


class DetallesCompraResponse(BaseModel):
    id: int
    idCompra: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float

    class Config:
        from_attributes = True
