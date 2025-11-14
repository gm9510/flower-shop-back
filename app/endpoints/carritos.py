from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para Carrito


@router.post("/carritos/", response_model=schemas.Carrito)
def create_carrito(carrito: schemas.CarritoCreate, db: Session = Depends(get_db)):
    db_carrito = models.Carrito(**carrito.model_dump())
    db.add(db_carrito)
    db.commit()
    db.refresh(db_carrito)
    return db_carrito


@router.get("/carritos/", response_model=List[schemas.Carrito])
def read_carritos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carritos = db.query(models.Carrito).offset(skip).limit(limit).all()
    return carritos


@router.get("/carritos/{carrito_id}", response_model=schemas.Carrito)
def read_carrito(carrito_id: int, db: Session = Depends(get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.id == carrito_id).first()
    if carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito


@router.put("/carritos/{carrito_id}", response_model=schemas.Carrito)
def update_carrito(carrito_id: int, carrito: schemas.CarritoUpdate, db: Session = Depends(get_db)):
    db_carrito = db.query(models.Carrito).filter(models.Carrito.id == carrito_id).first()
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    for key, value in carrito.model_dump().items():
        setattr(db_carrito, key, value)
    
    db.commit()
    db.refresh(db_carrito)
    return db_carrito


@router.delete("/carritos/{carrito_id}")
def delete_carrito(carrito_id: int, db: Session = Depends(get_db)):
    db_carrito = db.query(models.Carrito).filter(models.Carrito.id == carrito_id).first()
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    db.delete(db_carrito)
    db.commit()
    return {"message": "Carrito eliminado correctamente"}