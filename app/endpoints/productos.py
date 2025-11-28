from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para Producto


@router.post("/productos/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.get("/productos/", response_model=List[schemas.Producto])
def read_productos(
    skip: int = 0, 
    limit: int = 100,
    tipo: str = None,
    estado: str = None,
    nombre_like: str = None,
    codbarra: str = None,
    categoria: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Producto)
    
    if tipo is not None:
        query = query.filter(models.Producto.tipo == tipo)
    if estado is not None:
        query = query.filter(models.Producto.estado == estado)
    if nombre_like is not None:
        query = query.filter(models.Producto.nombre.like(f"%{nombre_like}%"))
    if codbarra is not None:
        query = query.filter(models.Producto.codbarra == codbarra)
    if categoria is not None:
        query = query.filter(models.Producto.categoria == categoria)
    
    productos = query.offset(skip).limit(limit).all()
    return productos


@router.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for key, value in producto.model_dump().items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado correctamente"}