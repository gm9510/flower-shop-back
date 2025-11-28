from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Endpoints para PedidoDetalle


@router.post("/pedidodetalles/", response_model=schemas.PedidoDetalle)
def create_pedidodetalle(pedidodetalle: schemas.PedidoDetalleCreate, db: Session = Depends(get_db)):
    db_pedidodetalle = models.PedidoDetalle(**pedidodetalle.model_dump())
    db.add(db_pedidodetalle)
    db.commit()
    db.refresh(db_pedidodetalle)
    return db_pedidodetalle


@router.get("/pedidodetalles/", response_model=List[schemas.PedidoDetalle])
def read_pedidodetalles(
    skip: int = 0,
    limit: int = 100,
    idPedido: int = None,
    idProducto: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.PedidoDetalle)

    if idPedido is not None:
        query = query.filter(models.PedidoDetalle.idPedido == idPedido)
    if idProducto is not None:
        query = query.filter(models.PedidoDetalle.idProducto == idProducto)

    pedidodetalles = query.offset(skip).limit(limit).all()
    return pedidodetalles


@router.get("/pedidodetalles/{pedidodetalle_id}", response_model=schemas.PedidoDetalle)
def read_pedidodetalle(pedidodetalle_id: int, db: Session = Depends(get_db)):
    pedidodetalle = db.query(models.PedidoDetalle).filter(models.PedidoDetalle.id == pedidodetalle_id).first()
    if pedidodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return pedidodetalle


@router.put("/pedidodetalles/{pedidodetalle_id}", response_model=schemas.PedidoDetalle)
def update_pedidodetalle(pedidodetalle_id: int, pedidodetalle: schemas.PedidoDetalleUpdate, db: Session = Depends(get_db)):
    db_pedidodetalle = db.query(models.PedidoDetalle).filter(models.PedidoDetalle.id == pedidodetalle_id).first()
    if db_pedidodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    for key, value in pedidodetalle.model_dump().items():
        setattr(db_pedidodetalle, key, value)
    
    db.commit()
    db.refresh(db_pedidodetalle)
    return db_pedidodetalle


@router.patch("/pedidodetalles/{pedidodetalle_id}/cantidad", response_model=schemas.PedidoDetalle)
def update_pedidodetalle_cantidad(pedidodetalle_id: int, cantidad: int, db: Session = Depends(get_db)):
    db_pedidodetalle = db.query(models.PedidoDetalle).filter(models.PedidoDetalle.id == pedidodetalle_id).first()
    if db_pedidodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

    db_pedidodetalle.cantidad = cantidad

    db.commit()
    db.refresh(db_pedidodetalle)
    return db_pedidodetalle


@router.delete("/pedidodetalles/{pedidodetalle_id}")
def delete_pedidodetalle(pedidodetalle_id: int, db: Session = Depends(get_db)):
    db_pedidodetalle = db.query(models.PedidoDetalle).filter(models.PedidoDetalle.id == pedidodetalle_id).first()
    if db_pedidodetalle is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    db.delete(db_pedidodetalle)
    db.commit()
    return {"message": "Detalle de pedido eliminado correctamente"}