from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum

class TipoDescuentoEnum(PyEnum):
    PORCENTAJE = "porcentaje"
    MONTO_FIJO = "monto_fijo"


# Modelo para la tabla pedidoCupon
class PedidoCupon(Base):
    __tablename__ = "pedidoCupon"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    tipoDescuento = Column(Enum(TipoDescuentoEnum), nullable=False)  # Este enum se define abajo
    valorDescuento = Column(Float(10, 2), nullable=False)
    validoDesde = Column(DateTime, nullable=True)
    validoHasta = Column(DateTime, nullable=True)
    limiteUso = Column(Integer, nullable=True)