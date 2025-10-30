from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)

    productos = relationship("Producto", back_populates="categoria")

class MetodoEnvio(Base):
    __tablename__ = "metodosEnvio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(DECIMAL(10, 2), nullable=False, default=0)
    tiempoEstimadoEntrega = Column(Integer)  # en días

    pedidos = relationship("Pedidos", back_populates="metodoEnvio")

class Cupon(Base):
    __tablename__ = "cupones"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    tipoDescuento = Column(Enum('porcentaje', 'monto_fijo', name='tipo_descuento_enum'), nullable=False)
    valorDescuento = Column(DECIMAL(10, 2), nullable=False)
    validoDesde = Column(Date)  # Cambiado a Date
    validoHasta = Column(Date)  # Cambiado a Date
    limiteUso = Column(Integer)

    pedidos = relationship("Pedidos", back_populates="cupon")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    categoriaId = Column(Integer, ForeignKey("categorias.id"))
    imagenUrl = Column(String(500))
    creadoEn = Column(DateTime, default=datetime.utcnow)
    actualizadoEn = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="productos")
    inventario = relationship("Inventario", back_populates="producto")
    carritos = relationship("CarritoCompras", back_populates="producto")
    itemsPedido = relationship("ItemsPedido", back_populates="producto")
    detallesCompra = relationship("DetallesCompra", back_populates="producto")

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    productoId = Column(Integer, ForeignKey("productos.id"))
    cantidadStock = Column(Integer, nullable=False)
    cantidadMinima = Column(Integer, default=0)
    ultimaActualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    producto = relationship("Producto", back_populates="inventario")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(Text)
    creadoEn = Column(DateTime, default=datetime.utcnow)

    carritos = relationship("CarritoCompras", back_populates="cliente")
    pedidos = relationship("Pedidos", back_populates="cliente")

class CarritoCompras(Base):
    __tablename__ = "carritoCompras"

    id = Column(Integer, primary_key=True, index=True)
    clienteId = Column(Integer, ForeignKey("clientes.id"))
    productoId = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False, default=1)
    agregadoEn = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="carritos")
    producto = relationship("Producto", back_populates="carritos")

class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    clienteId = Column(Integer, ForeignKey("clientes.id"))
    montoTotal = Column(DECIMAL(10, 2), nullable=False)
    estadoPedido = Column(Enum('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado', name='estado_pedido_enum'), default='pendiente')
    estadoPago = Column(Enum('pendiente', 'pagado', 'fallido', 'reembolsado', name='estado_pago_enum'), default='pendiente')
    metodoPago = Column(String(50))
    direccionEnvio = Column(Text)
    cuponId = Column(Integer, ForeignKey("cupones.id"))
    metodoEnvioId = Column(Integer, ForeignKey("metodosEnvio.id"))
    creadoEn = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="pedidos")
    cupon = relationship("Cupon", back_populates="pedidos")
    metodoEnvio = relationship("MetodoEnvio", back_populates="pedidos")
    itemsPedido = relationship("ItemsPedido", back_populates="pedido")
    pagos = relationship("Pagos", back_populates="pedido")

class ItemsPedido(Base):
    __tablename__ = "itemsPedido"

    id = Column(Integer, primary_key=True, index=True)
    pedidoId = Column(Integer, ForeignKey("pedidos.id"))
    productoId = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precioUnitario = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    pedido = relationship("Pedidos", back_populates="itemsPedido")
    producto = relationship("Producto", back_populates="itemsPedido")

class Pagos(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedidoId = Column(Integer, ForeignKey("pedidos.id"))
    pasarelaPagoId = Column(String(255), nullable=False)  # ID de la transacción en la pasarela
    monto = Column(DECIMAL(10, 2), nullable=False)
    estadoPago = Column(Enum('pendiente', 'completado', 'fallido', 'reembolsado', name='estado_pago_pago_enum'), default='pendiente')
    metodoPago = Column(String(50))
    transaccionId = Column(String(255))
    creadoEn = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedidos", back_populates="pagos")

# =====================
# NUEVAS TABLAS
# =====================

class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20))

class Entidad(Base):
    __tablename__ = "entidades"

    id = Column(Integer, primary_key=True, index=True)
    tipoEntidad = Column(Enum('cliente', 'proveedor', name='tipo_entidad_enum'), nullable=False)
    nombre = Column(String(100))
    apellido = Column(String(100))
    contacto = Column(String(255), nullable=False)
    telefono = Column(String(20))
    email = Column(String(255))
    direccion = Column(Text)

class Compras(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    idProveedor = Column(Integer, ForeignKey("entidades.id"))
    idSede = Column(Integer, ForeignKey("sedes.id"))
    total = Column(DECIMAL(10, 2), nullable=False)
    estadoCompra = Column(Enum('pendiente', 'recibida', 'cancelada', name='estado_compra_enum'), default='pendiente')
    creadoEn = Column(DateTime, default=datetime.utcnow)

    proveedor = relationship("Entidad")
    sede = relationship("Sede")
    detallesCompra = relationship("DetallesCompra", back_populates="compra")

class DetallesCompra(Base):
    __tablename__ = "detallesCompra"

    id = Column(Integer, primary_key=True, index=True)
    idCompra = Column(Integer, ForeignKey("compras.id"))
    productoId = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precioUnitario = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    compra = relationship("Compras", back_populates="detallesCompra")
    producto = relationship("Producto", back_populates="detallesCompra")