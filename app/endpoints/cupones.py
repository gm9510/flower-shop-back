from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Cupon
from app.schemas.cupon import CuponCreate, CuponResponse

router = APIRouter()

@router.get("/cupones", response_model=list[CuponResponse])
def get_cupones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cupones = db.query(Cupon).offset(skip).limit(limit).all()
    return cupones

@router.post("/cupones", response_model=CuponResponse)
def create_cupon(cupon: CuponCreate, db: Session = Depends(get_db)):
    db_cupon = Cupon(
        codigo=cupon.codigo,
        tipoDescuento=cupon.tipoDescuento,
        valorDescuento=cupon.valorDescuento,
        validoDesde=cupon.validoDesde,
        validoHasta=cupon.validoHasta,
        limiteUso=cupon.limiteUso
    )
    db.add(db_cupon)
    db.commit()
    db.refresh(db_cupon)
    return db_cupon