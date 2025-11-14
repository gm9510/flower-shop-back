from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para PedidoEnvio


@router.post("/pedidoenvios/", response_model=schemas.PedidoEnvio)
def create_pedidoenvio(pedidoenvio: schemas.PedidoEnvioCreate, db: Session = Depends(get_db)):
    db_pedidoenvio = models.PedidoEnvio(**pedidoenvio.model_dump())
    db.add(db_pedidoenvio)
    db.commit()
    db.refresh(db_pedidoenvio)
    return db_pedidoenvio


@router.get("/pedidoenvios/", response_model=List[schemas.PedidoEnvio])
def read_pedidoenvios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidoenvios = db.query(models.PedidoEnvio).offset(skip).limit(limit).all()
    return pedidoenvios


@router.get("/pedidoenvios/{pedidoenvio_id}", response_model=schemas.PedidoEnvio)
def read_pedidoenvio(pedidoenvio_id: int, db: Session = Depends(get_db)):
    pedidoenvio = db.query(models.PedidoEnvio).filter(models.PedidoEnvio.id == pedidoenvio_id).first()
    if pedidoenvio is None:
        raise HTTPException(status_code=404, detail="Método de envío no encontrado")
    return pedidoenvio


@router.put("/pedidoenvios/{pedidoenvio_id}", response_model=schemas.PedidoEnvio)
def update_pedidoenvio(pedidoenvio_id: int, pedidoenvio: schemas.PedidoEnvioUpdate, db: Session = Depends(get_db)):
    db_pedidoenvio = db.query(models.PedidoEnvio).filter(models.PedidoEnvio.id == pedidoenvio_id).first()
    if db_pedidoenvio is None:
        raise HTTPException(status_code=404, detail="Método de envío no encontrado")
    
    for key, value in pedidoenvio.model_dump().items():
        setattr(db_pedidoenvio, key, value)
    
    db.commit()
    db.refresh(db_pedidoenvio)
    return db_pedidoenvio


@router.delete("/pedidoenvios/{pedidoenvio_id}")
def delete_pedidoenvio(pedidoenvio_id: int, db: Session = Depends(get_db)):
    db_pedidoenvio = db.query(models.PedidoEnvio).filter(models.PedidoEnvio.id == pedidoenvio_id).first()
    if db_pedidoenvio is None:
        raise HTTPException(status_code=404, detail="Método de envío no encontrado")
    
    db.delete(db_pedidoenvio)
    db.commit()
    return {"message": "Método de envío eliminado correctamente"}