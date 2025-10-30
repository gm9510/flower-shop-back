from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Entidad
from app.schemas.entidad import EntidadCreate, EntidadResponse

router = APIRouter()

@router.get("/entidades", response_model=list[EntidadResponse])
def get_entidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entidades = db.query(Entidad).offset(skip).limit(limit).all()
    return entidades

@router.post("/entidades", response_model=EntidadResponse)
def create_entidad(entidad: EntidadCreate, db: Session = Depends(get_db)):
    db_entidad = Entidad(
        tipoEntidad=entidad.tipoEntidad,
        nombre=entidad.nombre,
        apellido=entidad.apellido,
        contacto=entidad.contacto,
        telefono=entidad.telefono,
        email=entidad.email,
        direccion=entidad.direccion
    )
    db.add(db_entidad)
    db.commit()
    db.refresh(db_entidad)
    return db_entidad