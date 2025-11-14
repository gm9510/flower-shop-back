from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla carrito
class Carrito(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    idEntidad = Column(Integer, ForeignKey("entidad.id"), nullable=True)
    sessionToken = Column(String(100), nullable=False)
    registro = Column(DateTime, default=func.now())

    # Relación con entidad
    entidad = relationship("Entidad", back_populates="carritos")
    # Relación con carritoDetalle
    detalles = relationship("CarritoDetalle", back_populates="carrito")