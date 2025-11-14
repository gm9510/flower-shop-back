from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para Inventario


@router.post("/inventarios/", response_model=schemas.Inventario)
def create_inventario(inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = models.Inventario(**inventario.model_dump())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario


@router.get("/inventarios/", response_model=List[schemas.Inventario])
def read_inventarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventarios = db.query(models.Inventario).offset(skip).limit(limit).all()
    return inventarios


@router.get("/inventarios/{inventario_id}", response_model=schemas.Inventario)
def read_inventario(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(models.Inventario).filter(models.Inventario.id == inventario_id).first()
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario


@router.put("/inventarios/{inventario_id}", response_model=schemas.Inventario)
def update_inventario(inventario_id: int, inventario: schemas.InventarioUpdate, db: Session = Depends(get_db)):
    db_inventario = db.query(models.Inventario).filter(models.Inventario.id == inventario_id).first()
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    for key, value in inventario.model_dump().items():
        setattr(db_inventario, key, value)
    
    db.commit()
    db.refresh(db_inventario)
    return db_inventario


@router.delete("/inventarios/{inventario_id}")
def delete_inventario(inventario_id: int, db: Session = Depends(get_db)):
    db_inventario = db.query(models.Inventario).filter(models.Inventario.id == inventario_id).first()
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    db.delete(db_inventario)
    db.commit()
    return {"message": "Inventario eliminado correctamente"}