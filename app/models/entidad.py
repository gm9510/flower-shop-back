from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

# Modelo para la tabla entidad
class Entidad(Base):
    __tablename__ = "entidad"

    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String(20), nullable=False, unique=True)
    dv = Column(Integer, nullable=True)
    nombre = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)
    estado = Column(Boolean, server_default="1")
    direccion = Column(String(200), nullable=True)
    
    carritos = relationship("Carrito", back_populates="entidad")
    compras = relationship("Compra", back_populates="entidad")
    pedidos = relationship("Pedido", back_populates="entidad")