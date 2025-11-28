from sqlalchemy import Column, Integer, String, Float
from app.database import Base


# Modelo para la tabla pedidoEnvio
class PedidoEnvio(Base):
    __tablename__ = "pedidoEnvio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(Float(10, 2), server_default="0.0")
    tiempoEstimadoEntrega = Column(Integer, nullable=True)