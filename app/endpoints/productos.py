from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Producto
from app.schemas.producto import ProductoCreate, ProductoResponse

router = APIRouter()

@router.get("/productos", response_model=list[ProductoResponse])
def get_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos

@router.post("/productos", response_model=ProductoResponse)
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