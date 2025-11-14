from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para ProductoEnsamble


@router.post("/productoensambles/", response_model=schemas.ProductoEnsamble)
def create_productoensamble(productoensamble: schemas.ProductoEnsambleCreate, db: Session = Depends(get_db)):
    db_productoensamble = models.ProductoEnsamble(**productoensamble.model_dump())
    db.add(db_productoensamble)
    db.commit()
    db.refresh(db_productoensamble)
    return db_productoensamble


@router.get("/productoensambles/", response_model=List[schemas.ProductoEnsamble])
def read_productoensambles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productoensambles = db.query(models.ProductoEnsamble).offset(skip).limit(limit).all()
    return productoensambles


@router.get("/productoensambles/{productoensamble_id}", response_model=schemas.ProductoEnsamble)
def read_productoensamble(productoensamble_id: int, db: Session = Depends(get_db)):
    productoensamble = db.query(models.ProductoEnsamble).filter(models.ProductoEnsamble.id == productoensamble_id).first()
    if productoensamble is None:
        raise HTTPException(status_code=404, detail="Producto ensamble no encontrado")
    return productoensamble


@router.put("/productoensambles/{productoensamble_id}", response_model=schemas.ProductoEnsamble)
def update_productoensamble(productoensamble_id: int, productoensamble: schemas.ProductoEnsambleUpdate, db: Session = Depends(get_db)):
    db_productoensamble = db.query(models.ProductoEnsamble).filter(models.ProductoEnsamble.id == productoensamble_id).first()
    if db_productoensamble is None:
        raise HTTPException(status_code=404, detail="Producto ensamble no encontrado")
    
    for key, value in productoensamble.model_dump().items():
        setattr(db_productoensamble, key, value)
    
    db.commit()
    db.refresh(db_productoensamble)
    return db_productoensamble


@router.delete("/productoensambles/{productoensamble_id}")
def delete_productoensamble(productoensamble_id: int, db: Session = Depends(get_db)):
    db_productoensamble = db.query(models.ProductoEnsamble).filter(models.ProductoEnsamble.id == productoensamble_id).first()
    if db_productoensamble is None:
        raise HTTPException(status_code=404, detail="Producto ensamble no encontrado")
    
    db.delete(db_productoensamble)
    db.commit()
    return {"message": "Producto ensamble eliminado correctamente"}