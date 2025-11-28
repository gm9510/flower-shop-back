from sqlalchemy import Column, Integer, String, Integer as SqlInt, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base


# Modelo para la tabla producto
class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=True)
    precioVenta = Column(SqlInt, nullable=True)
    tipo = Column(String(45), server_default='SIMPLE')
    categoria = Column(String(20), nullable=False)
    codbarra = Column(String(250), nullable=True)
    estado = Column(String(200), nullable=True)
    descripcion = Column(Text, nullable=True)
    imagenUrl = Column(String(1024), nullable=True)

    # Relación con carritoDetalle
    carrito_detalles = relationship("CarritoDetalle", back_populates="producto")
    # Relación con inventario
    inventario = relationship("Inventario", back_populates="producto")
    # Relación con compraDetalle
    compra_detalles = relationship("CompraDetalle", back_populates="producto")
    # Relación con pedidoDetalle
    pedido_detalles = relationship("PedidoDetalle", back_populates="producto")
    # Relación con productoEnsamble (como padre)
    ensambles_padre = relationship("ProductoEnsamble", back_populates="producto_padre", foreign_keys="ProductoEnsamble.idProductoPadre")
    # Relación con productoEnsamble (como hijo)
    ensambles_hijo = relationship("ProductoEnsamble", back_populates="producto_hijo", foreign_keys="ProductoEnsamble.idProductoHijo")