from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Inventario
from app.schemas.inventario import InventarioCreate, InventarioResponse

router = APIRouter()

@router.get("/inventario", response_model=list[InventarioResponse])
def get_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).offset(skip).limit(limit).all()
    return inventario

@router.post("/inventario", response_model=InventarioResponse)
def create_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = Inventario(
        productoId=inventario.productoId,
        cantidadStock=inventario.cantidadStock,
        cantidadMinima=inventario.cantidadMinima
    )
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario