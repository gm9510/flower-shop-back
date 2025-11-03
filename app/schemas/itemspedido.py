from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemsPedidoCreate(BaseModel):
    pedidoId: int = Field(..., description="ID del pedido al que pertenece este ítem")
    productoId: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad del producto en el pedido")
    precioUnitario: float = Field(..., gt=0, description="Precio unitario del producto")
    subtotal: float = Field(..., gt=0, description="Subtotal calculado (cantidad * precioUnitario)")

    class Config:
        json_schema_extra = {
            "example": {
                "pedidoId": 1,
                "productoId": 5,
                "cantidad": 3,
                "precioUnitario": 25.50,
                "subtotal": 76.50
            }
        }


class ItemsPedidoUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0, description="Nueva cantidad del producto")
    precioUnitario: Optional[float] = Field(None, gt=0, description="Nuevo precio unitario")
    subtotal: Optional[float] = Field(None, gt=0, description="Nuevo subtotal calculado")


class ItemsPedidoResponse(BaseModel):
    id: int
    pedidoId: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float

    class Config:
        from_attributes = True


class ItemsPedidoDetail(BaseModel):
    id: int
    pedidoId: int
    productoId: int
    cantidad: int
    precioUnitario: float
    subtotal: float
    pedido: Optional[dict] = Field(None, description="Información básica del pedido")
    producto: Optional[dict] = Field(None, description="Información básica del producto")

    class Config:
        from_attributes = True
