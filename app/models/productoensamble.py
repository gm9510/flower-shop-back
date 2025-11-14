from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla productoEnsamble
class ProductoEnsamble(Base):
    __tablename__ = "productoEnsamble"

    id = Column(Integer, primary_key=True, index=True)
    idProductoPadre = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Float(10, 2), nullable=False)
    idProductoHijo = Column(Integer, ForeignKey("producto.id"), nullable=False)

    # Relación con producto padre
    producto_padre = relationship("Producto", back_populates="ensambles_padre", foreign_keys=[idProductoPadre])
    # Relación con producto hijo
    producto_hijo = relationship("Producto", back_populates="ensambles_hijo", foreign_keys=[idProductoHijo])