from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla carritoDetalle
class CarritoDetalle(Base):
    __tablename__ = "carritoDetalle"

    id = Column(Integer, primary_key=True, index=True)
    idCarrito = Column(Integer, ForeignKey("carrito.id"), nullable=False)
    idProducto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precioUnitario = Column(Float(10, 2), nullable=False)

    # Relación con carrito
    carrito = relationship("Carrito", back_populates="detalles")
    # Relación con producto
    producto = relationship("Producto", back_populates="carrito_detalles")