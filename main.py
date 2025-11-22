from fastapi import FastAPI, Depends
from app.database import engine, Base
from app.endpoints import (
    entidades, productos, pedidos,
    carritos, carritodetalles,
    inventarios,
    compras, compradetalles, compraabonos,
    pedidodetalles, pedidopagos, pedidoenvios, pedidocupones,
    productoensambles
)  # Import your endpoints
from app.endpoints import auth
from app.auth.clerk_auth import get_current_user

app = FastAPI(
    title="MariaDB FastAPI Project",
    description="API con FastAPI y MariaDB",
    version="1.0.0"
)

# Create database tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Include routers with tags to ensure proper documentation
app.include_router(auth.router, tags=["auth"])  # Auth endpoints don't require authentication
app.include_router(entidades.router, prefix="/api", tags=["entidades"], dependencies=[Depends(get_current_user)])
app.include_router(productos.router, prefix="/api", tags=["productos"], dependencies=[Depends(get_current_user)])
app.include_router(pedidos.router, prefix="/api", tags=["pedidos"], dependencies=[Depends(get_current_user)])
app.include_router(carritos.router, prefix="/api", tags=["carritos"], dependencies=[Depends(get_current_user)])
app.include_router(carritodetalles.router, prefix="/api", tags=["carritodetalles"], dependencies=[Depends(get_current_user)])
app.include_router(inventarios.router, prefix="/api", tags=["inventarios"], dependencies=[Depends(get_current_user)])
app.include_router(compras.router, prefix="/api", tags=["compras"], dependencies=[Depends(get_current_user)])
app.include_router(compradetalles.router, prefix="/api", tags=["compradetalles"], dependencies=[Depends(get_current_user)])
app.include_router(compraabonos.router, prefix="/api", tags=["compraabonos"], dependencies=[Depends(get_current_user)])
app.include_router(pedidodetalles.router, prefix="/api", tags=["pedidodetalles"], dependencies=[Depends(get_current_user)])
app.include_router(pedidopagos.router, prefix="/api", tags=["pedidopagos"], dependencies=[Depends(get_current_user)])
app.include_router(pedidoenvios.router, prefix="/api", tags=["pedidoenvios"], dependencies=[Depends(get_current_user)])
app.include_router(pedidocupones.router, prefix="/api", tags=["pedidocupones"], dependencies=[Depends(get_current_user)])
app.include_router(productoensambles.router, prefix="/api", tags=["productoensambles"], dependencies=[Depends(get_current_user)])

@app.get("/", include_in_schema=False)  # Exclude from docs
def read_root():
    return {"message": "Bienvenido a la API con FastAPI y MariaDB"}

@app.get("/health", include_in_schema=False)  # Exclude from docs
def health_check():
    return {"status": "healthy"}