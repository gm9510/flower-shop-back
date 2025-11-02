from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PedidosCreate(BaseModel):
    clienteId: int = Field(..., description="ID del cliente que realiza el pedido")
    montoTotal: float = Field(..., gt=0, description="Monto total del pedido")
    estadoPedido: str = Field(default='pendiente', description="Estado del pedido")
    estadoPago: str = Field(default='pendiente', description="Estado del pago")
    metodoPago: Optional[str] = Field(None, description="Método de pago utilizado")
    direccionEnvio: Optional[str] = Field(None, description="Dirección de envío")
    cuponId: Optional[int] = Field(None, description="ID del cupón aplicado")
    metodoEnvioId: Optional[int] = Field(None, description="ID del método de envío")

    class Config:
        json_schema_extra = {
            "example": {
                "clienteId": 1,
                "montoTotal": 45.99,
                "estadoPedido": "pendiente",
                "estadoPago": "pendiente",
                "metodoPago": "tarjeta_credito",
                "direccionEnvio": "Av. Principal 123, Ciudad",
                "cuponId": 1,
                "metodoEnvioId": 1
            }
        }


class PedidosUpdate(BaseModel):
    montoTotal: Optional[float] = Field(None, gt=0, description="Monto total del pedido")
    estadoPedido: Optional[str] = Field(None, description="Estado del pedido: pendiente, procesando, enviado, entregado, cancelado")
    estadoPago: Optional[str] = Field(None, description="Estado del pago: pendiente, pagado, fallido, reembolsado")
    metodoPago: Optional[str] = Field(None, description="Método de pago utilizado")
    direccionEnvio: Optional[str] = Field(None, description="Dirección de envío")
    cuponId: Optional[int] = Field(None, description="ID del cupón aplicado")
    metodoEnvioId: Optional[int] = Field(None, description="ID del método de envío")

    class Config:
        json_schema_extra = {
            "example": {
                "estadoPedido": "procesando",
                "estadoPago": "pagado",
                "metodoPago": "transferencia_bancaria"
            }
        }


class PedidosResponse(BaseModel):
    id: int
    clienteId: int
    montoTotal: float
    estadoPedido: str
    estadoPago: str
    metodoPago: Optional[str] = None
    direccionEnvio: Optional[str] = None
    cuponId: Optional[int] = None
    metodoEnvioId: Optional[int] = None
    creadoEn: datetime

    class Config:
        from_attributes = True


class PedidosDetail(BaseModel):
    """Schema detallado para pedidos con información relacionada"""
    id: int
    clienteId: int
    montoTotal: float
    estadoPedido: str
    estadoPago: str
    metodoPago: Optional[str] = None
    direccionEnvio: Optional[str] = None
    cuponId: Optional[int] = None
    metodoEnvioId: Optional[int] = None
    creadoEn: datetime
    # Información relacionada (se puede agregar según necesidades)
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    cupon_codigo: Optional[str] = None
    metodo_envio_nombre: Optional[str] = None

    class Config:
        from_attributes = True
