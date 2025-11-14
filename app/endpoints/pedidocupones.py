from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para PedidoCupon


@router.post("/pedidocupones/", response_model=schemas.PedidoCupon)
def create_pedidocupon(pedidocupon: schemas.PedidoCuponCreate, db: Session = Depends(get_db)):
    db_pedidocupon = models.PedidoCupon(**pedidocupon.model_dump())
    db.add(db_pedidocupon)
    db.commit()
    db.refresh(db_pedidocupon)
    return db_pedidocupon


@router.get("/pedidocupones/", response_model=List[schemas.PedidoCupon])
def read_pedidocupones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidocupones = db.query(models.PedidoCupon).offset(skip).limit(limit).all()
    return pedidocupones


@router.get("/pedidocupones/{pedidocupon_id}", response_model=schemas.PedidoCupon)
def read_pedidocupon(pedidocupon_id: int, db: Session = Depends(get_db)):
    pedidocupon = db.query(models.PedidoCupon).filter(models.PedidoCupon.id == pedidocupon_id).first()
    if pedidocupon is None:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    return pedidocupon


@router.put("/pedidocupones/{pedidocupon_id}", response_model=schemas.PedidoCupon)
def update_pedidocupon(pedidocupon_id: int, pedidocupon: schemas.PedidoCuponUpdate, db: Session = Depends(get_db)):
    db_pedidocupon = db.query(models.PedidoCupon).filter(models.PedidoCupon.id == pedidocupon_id).first()
    if db_pedidocupon is None:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    
    for key, value in pedidocupon.model_dump().items():
        setattr(db_pedidocupon, key, value)
    
    db.commit()
    db.refresh(db_pedidocupon)
    return db_pedidocupon


@router.delete("/pedidocupones/{pedidocupon_id}")
def delete_pedidocupon(pedidocupon_id: int, db: Session = Depends(get_db)):
    db_pedidocupon = db.query(models.PedidoCupon).filter(models.PedidoCupon.id == pedidocupon_id).first()
    if db_pedidocupon is None:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    
    db.delete(db_pedidocupon)
    db.commit()
    return {"message": "Cupón eliminado correctamente"}