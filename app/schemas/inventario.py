from pydantic import BaseModel


class InventarioCreate(BaseModel):
    productoId: int
    cantidadStock: int
    cantidadMinima: int = 0


class InventarioResponse(BaseModel):
    id: int
    productoId: int
    cantidadStock: int
    cantidadMinima: int

    class Config:
        from_attributes = True
