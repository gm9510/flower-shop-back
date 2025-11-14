from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para Compra


@router.post("/compras/", response_model=schemas.Compra)
def create_compra(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    db_compra = models.Compra(**compra.model_dump())
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra


@router.get("/compras/", response_model=List[schemas.Compra])
def read_compras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    compras = db.query(models.Compra).offset(skip).limit(limit).all()
    return compras


@router.get("/compras/{compra_id}", response_model=schemas.Compra)
def read_compra(compra_id: int, db: Session = Depends(get_db)):
    compra = db.query(models.Compra).filter(models.Compra.id == compra_id).first()
    if compra is None:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra


@router.put("/compras/{compra_id}", response_model=schemas.Compra)
def update_compra(compra_id: int, compra: schemas.CompraUpdate, db: Session = Depends(get_db)):
    db_compra = db.query(models.Compra).filter(models.Compra.id == compra_id).first()
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    
    for key, value in compra.model_dump().items():
        setattr(db_compra, key, value)
    
    db.commit()
    db.refresh(db_compra)
    return db_compra


@router.delete("/compras/{compra_id}")
def delete_compra(compra_id: int, db: Session = Depends(get_db)):
    db_compra = db.query(models.Compra).filter(models.Compra.id == compra_id).first()
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    
    db.delete(db_compra)
    db.commit()
    return {"message": "Compra eliminada correctamente"}