from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla pedidoDetalle
class PedidoDetalle(Base):
    __tablename__ = "pedidoDetalle"

    id = Column(Integer, primary_key=True, index=True)
    idPedido = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    idProducto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precioUnitario = Column(Float(10, 2), nullable=False)
    resigstro = Column(DateTime, nullable=True)  # Nota: hay un error tipográfico en el esquema original

    # Relación con pedido
    pedido = relationship("Pedido", back_populates="detalles")
    # Relación con producto
    producto = relationship("Producto", back_populates="pedido_detalles")