from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Modelo para la tabla entidad
class Entidad(Base):
    __tablename__ = "entidad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    carritos = relationship("Carrito", back_populates="entidad")
    compras = relationship("Compra", back_populates="entidad")
    pedidos = relationship("Pedido", back_populates="entidad")