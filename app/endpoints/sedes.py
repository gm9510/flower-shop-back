from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Sede
from app.schemas.sede import SedeCreate, SedeResponse

router = APIRouter()

@router.get("/sedes", response_model=list[SedeResponse])
def get_sedes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sedes = db.query(Sede).offset(skip).limit(limit).all()
    return sedes

@router.post("/sedes", response_model=SedeResponse)
def create_sede(sede: SedeCreate, db: Session = Depends(get_db)):
    db_sede = Sede(
        nombre=sede.nombre,
        direccion=sede.direccion,
        telefono=sede.telefono
    )
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede