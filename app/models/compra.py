from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum


# Enumeraciones para las tablas
class MetodoPagoEnum(str, Enum):
    contado = "DE CONTADO"
    credito = "A CREDITO"


class OpcionPagoEnum(str, Enum):
    efectivo = "efectivo"
    transferencia = "trasnferencia"


# Modelo para la tabla compra
class Compra(Base):
    __tablename__ = "compra"

    id = Column(Integer, primary_key=True, index=True)
    idEntidad = Column(Integer, ForeignKey("entidad.id"), nullable=False)
    factura = Column(String(50), nullable=True)
    subTotal = Column(Float(15, 2), nullable=False)
    descuento = Column(Float(15, 2), server_default="0.0")
    total = Column(Float(15, 2), nullable=False)
    saldo = Column(Float(15, 2), server_default="0.0")
    metodoPago = Column(String(15), server_default="DE CONTADO")
    fechaLimite = Column(Date, nullable=True)
    efectivo = Column(Float(12, 2), nullable=True)
    transferencia = Column(Float(12, 2), nullable=True)
    observacion = Column(String(100), nullable=True)
    usuario = Column(String(10), nullable=True)
    registro = Column(DateTime, nullable=False)

    # Relación con entidad
    entidad = relationship("Entidad", back_populates="compras")
    # Relación con compraDetalle
    detalles = relationship("CompraDetalle", back_populates="compra")
    # Relación con compraAbono
    abonos = relationship("CompraAbono", back_populates="compra")