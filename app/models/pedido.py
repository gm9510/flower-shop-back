from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum


# Enumeraciones para las tablas
class EstadoPedidoEnum(PyEnum):
    pendiente = "pendiente"
    procesando = "procesando"
    enviado = "enviado"
    entregado = "entregado"
    cancelado = "cancelado"


class EstadoPagoEnum(PyEnum):
    pendiente = "pendiente"
    pagado = "pagado"
    fallido = "fallido"
    reembolsado = "reembolsado"


# Modelo para la tabla pedido
class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True)
    numeroFactura = Column(Integer, nullable=True)
    idEntidad = Column(Integer, ForeignKey("entidad.id"), nullable=False)
    subTotal = Column(Float(15, 2), nullable=False)
    descuento = Column(Float(15, 2), nullable=True)
    montoTotal = Column(Float(10, 2), nullable=False)
    saldo = Column(Float(15, 2), nullable=True)
    estadoPedido = Column(Enum(EstadoPedidoEnum), default=EstadoPedidoEnum.pendiente)
    estadoPago = Column(Enum(EstadoPagoEnum), default=EstadoPagoEnum.pendiente)
    metodoPago = Column(String(15), default="DE CONTADO")
    direccionEnvio = Column(Text, nullable=True)
    idCupon = Column(Integer, nullable=True)
    idEnvio = Column(Integer, nullable=True)
    efectivo = Column(Integer, nullable=True)
    transferencia = Column(Integer, nullable=True)
    usuario = Column(String(10), nullable=True)
    registro = Column(DateTime, nullable=True)

    # Relación con entidad
    entidad = relationship("Entidad", back_populates="pedidos")
    # Relación con pedidoDetalle
    detalles = relationship("PedidoDetalle", back_populates="pedido")
    # Relación con pedidoPago
    pagos = relationship("PedidoPago", back_populates="pedido")