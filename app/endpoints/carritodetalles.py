from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para CarritoDetalle


@router.post("/carritodetalles/", response_model=schemas.CarritoDetalle)
def create_carritodetalle(carritodetalle: schemas.CarritoDetalleCreate, db: Session = Depends(get_db)):
    db_carritodetalle = models.CarritoDetalle(**carritodetalle.model_dump())
    db.add(db_carritodetalle)
    db.commit()
    db.refresh(db_carritodetalle)
    return db_carritodetalle


@router.get("/carritodetalles/", response_model=List[schemas.CarritoDetalle])
def read_carritodetalles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carritodetalles = db.query(models.CarritoDetalle).offset(skip).limit(limit).all()
    return carritodetalles


@router.get("/carritodetalles/{carritodetalle_id}", response_model=schemas.CarritoDetalle)
def read_carritodetalle(carritodetalle_id: int, db: Session = Depends(get_db)):
    carritodetalle = db.query(models.CarritoDetalle).filter(models.CarritoDetalle.id == carritodetalle_id).first()
    if carritodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de carrito no encontrado")
    return carritodetalle


@router.put("/carritodetalles/{carritodetalle_id}", response_model=schemas.CarritoDetalle)
def update_carritodetalle(carritodetalle_id: int, carritodetalle: schemas.CarritoDetalleUpdate, db: Session = Depends(get_db)):
    db_carritodetalle = db.query(models.CarritoDetalle).filter(models.CarritoDetalle.id == carritodetalle_id).first()
    if db_carritodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de carrito no encontrado")
    
    for key, value in carritodetalle.model_dump().items():
        setattr(db_carritodetalle, key, value)
    
    db.commit()
    db.refresh(db_carritodetalle)
    return db_carritodetalle


@router.delete("/carritodetalles/{carritodetalle_id}")
def delete_carritodetalle(carritodetalle_id: int, db: Session = Depends(get_db)):
    db_carritodetalle = db.query(models.CarritoDetalle).filter(models.CarritoDetalle.id == carritodetalle_id).first()
    if db_carritodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de carrito no encontrado")
    
    db.delete(db_carritodetalle)
    db.commit()
    return {"message": "Detalle de carrito eliminado correctamente"}