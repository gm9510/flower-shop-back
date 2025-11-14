from fastapi import FastAPI
from app.database import engine, Base
from app.endpoints import (
    entidades, productos, pedidos,
    carritos, carritodetalles,
    inventarios,
    compras, compradetalles, compraabonos,
    pedidodetalles, pedidopagos, pedidoenvios, pedidocupones,
    productoensambles
)  # Import your endpoints

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
app.include_router(entidades.router, prefix="/api", tags=["entidades"])
app.include_router(productos.router, prefix="/api", tags=["productos"])
app.include_router(pedidos.router, prefix="/api", tags=["pedidos"])
app.include_router(carritos.router, prefix="/api", tags=["carritos"])
app.include_router(carritodetalles.router, prefix="/api", tags=["carritodetalles"])
app.include_router(inventarios.router, prefix="/api", tags=["inventarios"])
app.include_router(compras.router, prefix="/api", tags=["compras"])
app.include_router(compradetalles.router, prefix="/api", tags=["compradetalles"])
app.include_router(compraabonos.router, prefix="/api", tags=["compraabonos"])
app.include_router(pedidodetalles.router, prefix="/api", tags=["pedidodetalles"])
app.include_router(pedidopagos.router, prefix="/api", tags=["pedidopagos"])
app.include_router(pedidoenvios.router, prefix="/api", tags=["pedidoenvios"])
app.include_router(pedidocupones.router, prefix="/api", tags=["pedidocupones"])
app.include_router(productoensambles.router, prefix="/api", tags=["productoensambles"])

@app.get("/", include_in_schema=False)  # Exclude from docs
def read_root():
    return {"message": "Bienvenido a la API con FastAPI y MariaDB"}

@app.get("/health", include_in_schema=False)  # Exclude from docs
def health_check():
    return {"status": "healthy"}