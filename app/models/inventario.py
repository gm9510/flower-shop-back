from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla inventario
class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    idProducto = Column(Integer, ForeignKey("producto.id"), nullable=True)
    stock = Column(Float(12, 2), server_default="0.0")

    # Relación con producto
    producto = relationship("Producto", back_populates="inventario")