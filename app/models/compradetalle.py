from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla compraDetalle
class CompraDetalle(Base):
    __tablename__ = "compraDetalle"

    id = Column(Integer, primary_key=True, index=True)
    idCompra = Column(Integer, ForeignKey("compra.id"), nullable=False)
    idProducto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    costo = Column(Float(10, 2), nullable=False)
    iva = Column(Integer, default=0)
    costoIva = Column(Float(10, 2), nullable=False)
    totalUnitario = Column(Float(15, 2), nullable=True)
    precioVenta = Column(Float(10, 2), nullable=True)

    # Relación con compra
    compra = relationship("Compra", back_populates="detalles")
    # Relación con producto
    producto = relationship("Producto", back_populates="compra_detalles")