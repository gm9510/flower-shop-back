from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para PedidoPago


@router.post("/pedidopagos/", response_model=schemas.PedidoPago)
def create_pedidopago(pedidopago: schemas.PedidoPagoCreate, db: Session = Depends(get_db)):
    db_pedidopago = models.PedidoPago(**pedidopago.model_dump())
    db.add(db_pedidopago)
    db.commit()
    db.refresh(db_pedidopago)
    return db_pedidopago


@router.get("/pedidopagos/", response_model=List[schemas.PedidoPago])
def read_pedidopagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidopagos = db.query(models.PedidoPago).offset(skip).limit(limit).all()
    return pedidopagos


@router.get("/pedidopagos/{pedidopago_id}", response_model=schemas.PedidoPago)
def read_pedidopago(pedidopago_id: int, db: Session = Depends(get_db)):
    pedidopago = db.query(models.PedidoPago).filter(models.PedidoPago.id == pedidopago_id).first()
    if pedidopago is None:
        raise HTTPException(status_code=404, detail="Pago de pedido no encontrado")
    return pedidopago


@router.put("/pedidopagos/{pedidopago_id}", response_model=schemas.PedidoPago)
def update_pedidopago(pedidopago_id: int, pedidopago: schemas.PedidoPagoUpdate, db: Session = Depends(get_db)):
    db_pedidopago = db.query(models.PedidoPago).filter(models.PedidoPago.id == pedidopago_id).first()
    if db_pedidopago is None:
        raise HTTPException(status_code=404, detail="Pago de pedido no encontrado")
    
    for key, value in pedidopago.model_dump().items():
        setattr(db_pedidopago, key, value)
    
    db.commit()
    db.refresh(db_pedidopago)
    return db_pedidopago


@router.delete("/pedidopagos/{pedidopago_id}")
def delete_pedidopago(pedidopago_id: int, db: Session = Depends(get_db)):
    db_pedidopago = db.query(models.PedidoPago).filter(models.PedidoPago.id == pedidopago_id).first()
    if db_pedidopago is None:
        raise HTTPException(status_code=404, detail="Pago de pedido no encontrado")
    
    db.delete(db_pedidopago)
    db.commit()
    return {"message": "Pago de pedido eliminado correctamente"}