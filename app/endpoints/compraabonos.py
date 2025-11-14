from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para CompraAbono


@router.post("/compraabonos/", response_model=schemas.CompraAbono)
def create_compraabono(compraabono: schemas.CompraAbonoCreate, db: Session = Depends(get_db)):
    db_compraabono = models.CompraAbono(**compraabono.model_dump())
    db.add(db_compraabono)
    db.commit()
    db.refresh(db_compraabono)
    return db_compraabono


@router.get("/compraabonos/", response_model=List[schemas.CompraAbono])
def read_compraabonos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    compraabonos = db.query(models.CompraAbono).offset(skip).limit(limit).all()
    return compraabonos


@router.get("/compraabonos/{compraabono_id}", response_model=schemas.CompraAbono)
def read_compraabono(compraabono_id: int, db: Session = Depends(get_db)):
    compraabono = db.query(models.CompraAbono).filter(models.CompraAbono.id == compraabono_id).first()
    if compraabono is None:
        raise HTTPException(status_code=404, detail="Abono de compra no encontrado")
    return compraabono


@router.put("/compraabonos/{compraabono_id}", response_model=schemas.CompraAbono)
def update_compraabono(compraabono_id: int, compraabono: schemas.CompraAbonoUpdate, db: Session = Depends(get_db)):
    db_compraabono = db.query(models.CompraAbono).filter(models.CompraAbono.id == compraabono_id).first()
    if db_compraabono is None:
        raise HTTPException(status_code=404, detail="Abono de compra no encontrado")
    
    for key, value in compraabono.model_dump().items():
        setattr(db_compraabono, key, value)
    
    db.commit()
    db.refresh(db_compraabono)
    return db_compraabono


@router.delete("/compraabonos/{compraabono_id}")
def delete_compraabono(compraabono_id: int, db: Session = Depends(get_db)):
    db_compraabono = db.query(models.CompraAbono).filter(models.CompraAbono.id == compraabono_id).first()
    if db_compraabono is None:
        raise HTTPException(status_code=404, detail="Abono de compra no encontrado")
    
    db.delete(db_compraabono)
    db.commit()
    return {"message": "Abono de compra eliminado correctamente"}