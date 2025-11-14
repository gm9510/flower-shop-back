from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para CompraDetalle


@router.post("/compradetalles/", response_model=schemas.CompraDetalle)
def create_compradetalle(compradetalle: schemas.CompraDetalleCreate, db: Session = Depends(get_db)):
    db_compradetalle = models.CompraDetalle(**compradetalle.model_dump())
    db.add(db_compradetalle)
    db.commit()
    db.refresh(db_compradetalle)
    return db_compradetalle


@router.get("/compradetalles/", response_model=List[schemas.CompraDetalle])
def read_compradetalles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    compradetalles = db.query(models.CompraDetalle).offset(skip).limit(limit).all()
    return compradetalles


@router.get("/compradetalles/{compradetalle_id}", response_model=schemas.CompraDetalle)
def read_compradetalle(compradetalle_id: int, db: Session = Depends(get_db)):
    compradetalle = db.query(models.CompraDetalle).filter(models.CompraDetalle.id == compradetalle_id).first()
    if compradetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de compra no encontrado")
    return compradetalle


@router.put("/compradetalles/{compradetalle_id}", response_model=schemas.CompraDetalle)
def update_compradetalle(compradetalle_id: int, compradetalle: schemas.CompraDetalleUpdate, db: Session = Depends(get_db)):
    db_compradetalle = db.query(models.CompraDetalle).filter(models.CompraDetalle.id == compradetalle_id).first()
    if db_compradetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de compra no encontrado")
    
    for key, value in compradetalle.model_dump().items():
        setattr(db_compradetalle, key, value)
    
    db.commit()
    db.refresh(db_compradetalle)
    return db_compradetalle


@router.delete("/compradetalles/{compradetalle_id}")
def delete_compradetalle(compradetalle_id: int, db: Session = Depends(get_db)):
    db_compradetalle = db.query(models.CompraDetalle).filter(models.CompraDetalle.id == compradetalle_id).first()
    if db_compradetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de compra no encontrado")
    
    db.delete(db_compradetalle)
    db.commit()
    return {"message": "Detalle de compra eliminado correctamente"}