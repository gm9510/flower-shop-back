from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum

class OpcionPagoEnum(PyEnum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"


# Modelo para la tabla compraAbono
class CompraAbono(Base):
    __tablename__ = "compraAbono"

    id = Column(Integer, primary_key=True, index=True)
    idCompra = Column(Integer, ForeignKey("compra.id"), nullable=False)
    valor = Column(Float(32, 2), nullable=False)
    opcionPago = Column(Enum(OpcionPagoEnum), default=OpcionPagoEnum.EFECTIVO)  # Este enum se define en la tabla compra
    registro = Column(DateTime, nullable=False)
    usuario = Column(String(15), nullable=True)

    # Relación con compra
    compra = relationship("Compra", back_populates="abonos")