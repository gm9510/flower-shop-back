from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.auth.clerk_auth import get_current_user
from app.database import get_db

router = APIRouter()

# Endpoints para Pedido


@router.post("/pedidos/", response_model=schemas.Pedido)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_pedido = models.Pedido(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.get("/pedidos/", response_model=List[schemas.Pedido])
def read_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedido).offset(skip).limit(limit).all()
    return pedidos


@router.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def update_pedido(pedido_id: int, pedido: schemas.PedidoUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    for key, value in pedido.model_dump().items():
        setattr(db_pedido, key, value)
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.delete("/pedidos/{pedido_id}")
def delete_pedido(pedido_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    db.delete(db_pedido)
    db.commit()
    return {"message": "Pedido eliminado correctamente"}