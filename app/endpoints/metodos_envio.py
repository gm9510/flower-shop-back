from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import MetodoEnvio
from app.schemas.metodoenvio import MetodoEnvioCreate, MetodoEnvioResponse

router = APIRouter()

@router.get("/metodos-envio", response_model=list[MetodoEnvioResponse])
def get_metodos_envio(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metodos = db.query(MetodoEnvio).offset(skip).limit(limit).all()
    return metodos

@router.post("/metodos-envio", response_model=MetodoEnvioResponse)
def create_metodo_envio(metodo: MetodoEnvioCreate, db: Session = Depends(get_db)):
    db_metodo = MetodoEnvio(
        nombre=metodo.nombre,
        costo=metodo.costo,
        tiempoEstimadoEntrega=metodo.tiempoEstimadoEntrega
    )
    db.add(db_metodo)
    db.commit()
    db.refresh(db_metodo)
    return db_metodo