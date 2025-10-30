from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import date
import os

from app.database import engine, get_db
from app.models import Categoria, Producto, Cliente, Inventario, Cupon, MetodoEnvio, Pedidos, ItemsPedido, Pagos, Sede, Entidad, Compras, DetallesCompra

# Create tables
from app.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Floristería con MariaDB",
    description="API para la gestión de una floristería",
    version="1.0.0"
)

# Pydantic models
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoriaId: Optional[int] = None
    imagenUrl: Optional[str] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoriaId: Optional[int] = None
    imagenUrl: Optional[str] = None

    class Config:
        from_attributes = True

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

    class Config:
        from_attributes = True

class InventarioCreate(BaseModel):
    productoId: int
    cantidadStock: int
    cantidadMinima: int = 0

class InventarioResponse(BaseModel):
    id: int
    productoId: int
    cantidadStock: int
    cantidadMinima: int

    class Config:
        from_attributes = True

class CuponCreate(BaseModel):
    codigo: str
    tipoDescuento: str  # 'porcentaje' o 'monto_fijo'
    valorDescuento: float
    validoDesde: Optional[date] = None
    validoHasta: Optional[date] = None
    limiteUso: Optional[int] = None

class CuponResponse(BaseModel):
    id: int
    codigo: str
    tipoDescuento: str
    valorDescuento: float
    validoDesde: Optional[date] = None
    validoHasta: Optional[date] = None
    limiteUso: Optional[int] = None

    class Config:
        from_attributes = True

class MetodoEnvioCreate(BaseModel):
    nombre: str
    costo: float
    tiempoEstimadoEntrega: Optional[int] = None

class MetodoEnvioResponse(BaseModel):
    id: int
    nombre: str
    costo: float
    tiempoEstimadoEntrega: Optional[int] = None

    class Config:
        from_attributes = True

# Nuevos modelos para las tablas adicionales

class SedeCreate(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None

class SedeResponse(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: Optional[str] = None

    class Config:
        from_attributes = True

class EntidadCreate(BaseModel):
    tipoEntidad: str  # 'cliente' o 'proveedor'
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contacto: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class EntidadResponse(BaseModel):
    id: int
    tipoEntidad: str
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contacto: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "API de la Floristería con MariaDB"}

@app.get("/categorias", response_model=list[CategoriaResponse])
def get_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias

@app.post("/categorias", response_model=CategoriaResponse)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/productos", response_model=list[ProductoResponse])
def get_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos

@app.post("/productos", response_model=ProductoResponse)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        categoriaId=producto.categoriaId,
        imagenUrl=producto.imagenUrl
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/clientes", response_model=list[ClienteResponse])
def get_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes

@app.post("/clientes", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = Cliente(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/inventario", response_model=list[InventarioResponse])
def get_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).offset(skip).limit(limit).all()
    return inventario

@app.post("/inventario", response_model=InventarioResponse)
def create_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = Inventario(
        productoId=inventario.productoId,
        cantidadStock=inventario.cantidadStock,
        cantidadMinima=inventario.cantidadMinima
    )
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@app.get("/cupones", response_model=list[CuponResponse])
def get_cupones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cupones = db.query(Cupon).offset(skip).limit(limit).all()
    return cupones

@app.post("/cupones", response_model=CuponResponse)
def create_cupon(cupon: CuponCreate, db: Session = Depends(get_db)):
    db_cupon = Cupon(
        codigo=cupon.codigo,
        tipoDescuento=cupon.tipoDescuento,
        valorDescuento=cupon.valorDescuento,
        validoDesde=cupon.validoDesde,
        validoHasta=cupon.validoHasta,
        limiteUso=cupon.limiteUso
    )
    db.add(db_cupon)
    db.commit()
    db.refresh(db_cupon)
    return db_cupon

@app.get("/metodos-envio", response_model=list[MetodoEnvioResponse])
def get_metodos_envio(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metodos = db.query(MetodoEnvio).offset(skip).limit(limit).all()
    return metodos

@app.post("/metodos-envio", response_model=MetodoEnvioResponse)
def create_metodo_envio(metodo: MetodoEnvioCreate, db: Session = Depends(get_db)):
    db_metodo = MetodoEnvio(
        nombre=metodo.nombre,
        costo=metodo.costo,
        tiempoEstimadoEntrega=metodo.tiempoEstimadoEntrega
    )
    db.add(db_metodo)
    db.commit()
    db.refresh(db_metodo)
    return db_metodo

# Nuevos endpoints para las tablas adicionales

@app.get("/sedes", response_model=list[SedeResponse])
def get_sedes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sedes = db.query(Sede).offset(skip).limit(limit).all()
    return sedes

@app.post("/sedes", response_model=SedeResponse)
def create_sede(sede: SedeCreate, db: Session = Depends(get_db)):
    db_sede = Sede(
        nombre=sede.nombre,
        direccion=sede.direccion,
        telefono=sede.telefono
    )
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

@app.get("/entidades", response_model=list[EntidadResponse])
def get_entidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entidades = db.query(Entidad).offset(skip).limit(limit).all()
    return entidades

@app.post("/entidades", response_model=EntidadResponse)
def create_entidad(entidad: EntidadCreate, db: Session = Depends(get_db)):
    db_entidad = Entidad(
        tipoEntidad=entidad.tipoEntidad,
        nombre=entidad.nombre,
        apellido=entidad.apellido,
        contacto=entidad.contacto,
        telefono=entidad.telefono,
        email=entidad.email,
        direccion=entidad.direccion
    )
    db.add(db_entidad)
    db.commit()
    db.refresh(db_entidad)
    return db_entidad

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}