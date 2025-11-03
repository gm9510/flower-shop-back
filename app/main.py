from fastapi import APIRouter, FastAPI
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.endpoints.categorias import router as categorias_router
from app.endpoints.productos import router as productos_router
from app.endpoints.clientes import router as clientes_router
from app.endpoints.inventario import router as inventario_router
from app.endpoints.cupones import router as cupones_router
from app.endpoints.metodos_envio import router as metodos_envio_router
from app.endpoints.sedes import router as sedes_router
from app.endpoints.entidades import router as entidades_router
from app.endpoints.pedidos import router as pedidos_router
from app.endpoints.itemspedido import router as itemspedido_router

# Create tables
from app.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Floristería con MariaDB",
    description="API para la gestión de una floristería",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods for CORS requests
    allow_headers=["*"],  # Allows all headers for CORS requests
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
api_router.include_router(pedidos_router, tags=["pedidos"])
api_router.include_router(itemspedido_router, tags=["items-pedido"])
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "API de la Floristería con MariaDB"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}