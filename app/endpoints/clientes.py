from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter()

@router.get("/clientes", response_model=list[ClienteResponse])
def get_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes

@router.post("/clientes", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = Cliente(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente