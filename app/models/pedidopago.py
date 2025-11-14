from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum

class OpcionPagoEnum(PyEnum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"


class EstadoPagoEnum(PyEnum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"

# Modelo para la tabla pedidoPago
class PedidoPago(Base):
    __tablename__ = "pedidoPago"

    id = Column(Integer, primary_key=True, index=True)
    idPedido = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    pasarelaPagoId = Column(String(255), nullable=False)
    monto = Column(Float(10, 2), nullable=False)
    estadoPago = Column(Enum(EstadoPagoEnum), default=EstadoPagoEnum.PENDIENTE)  # Este enum se define en la tabla pedido
    opcionPago = Column(Enum(OpcionPagoEnum), default=OpcionPagoEnum.EFECTIVO)  # Este enum se define en la tabla compra
    idTransaccion = Column(String(255), nullable=True)
    usuario = Column(String(15), nullable=True)
    registro = Column(DateTime, default=func.now())

    # Relación con pedido
    pedido = relationship("Pedido", back_populates="pagos")