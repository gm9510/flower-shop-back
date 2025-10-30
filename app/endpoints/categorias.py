from fastapi import APIRouter
from app.models.models import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends

router = APIRouter()

@router.get("/categorias", response_model=list[CategoriaResponse])
def get_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias

@router.post("/categorias", response_model=CategoriaResponse)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria