from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para Entidad


@router.post("/entidades/", response_model=schemas.Entidad)
def create_entidad(entidad: schemas.EntidadCreate, db: Session = Depends(get_db)):
    db_entidad = models.Entidad(**entidad.model_dump())
    db.add(db_entidad)
    db.commit()
    db.refresh(db_entidad)
    return db_entidad


@router.get("/entidades/", response_model=List[schemas.Entidad])
def read_entidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entidades = db.query(models.Entidad).offset(skip).limit(limit).all()
    return entidades


@router.get("/entidades/{entidad_id}", response_model=schemas.Entidad)
def read_entidad(entidad_id: int, db: Session = Depends(get_db)):
    entidad = db.query(models.Entidad).filter(models.Entidad.id == entidad_id).first()
    if entidad is None:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
    return entidad


@router.put("/entidades/{entidad_id}", response_model=schemas.Entidad)
def update_entidad(entidad_id: int, entidad: schemas.EntidadUpdate, db: Session = Depends(get_db)):
    db_entidad = db.query(models.Entidad).filter(models.Entidad.id == entidad_id).first()
    if db_entidad is None:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
    
    for key, value in entidad.model_dump().items():
        setattr(db_entidad, key, value)
    
    db.commit()
    db.refresh(db_entidad)
    return db_entidad


@router.delete("/entidades/{entidad_id}")
def delete_entidad(entidad_id: int, db: Session = Depends(get_db)):
    db_entidad = db.query(models.Entidad).filter(models.Entidad.id == entidad_id).first()
    if db_entidad is None:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
    
    db.delete(db_entidad)
    db.commit()
    return {"message": "Entidad eliminada correctamente"}