from fastapi import APIRouter, FastAPI
from app.database import engine

# Import routers
from app.endpoints.categorias import router as categorias_router
from app.endpoints.productos import router as productos_router
from app.endpoints.clientes import router as clientes_router
from app.endpoints.inventario import router as inventario_router
from app.endpoints.cupones import router as cupones_router
from app.endpoints.metodos_envio import router as metodos_envio_router
from app.endpoints.sedes import router as sedes_router
from app.endpoints.entidades import router as entidades_router

# Create tables
from app.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Floristería con MariaDB",
    description="API para la gestión de una floristería",
    version="1.0.0"
)

api_router = APIRouter()
api_router.include_router(categorias_router, tags=["categorias"])
api_router.include_router(productos_router, tags=["productos"])
api_router.include_router(clientes_router, tags=["clientes"])
api_router.include_router(inventario_router, tags=["inventario"])
api_router.include_router(cupones_router, tags=["cupones"])
api_router.include_router(metodos_envio_router, tags=["metodos-envio"])
api_router.include_router(sedes_router, tags=["sedes"])
api_router.include_router(entidades_router, tags=["entidades"])
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "API de la Floristería con MariaDB"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}