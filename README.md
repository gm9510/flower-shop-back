# Proyecto FastAPI con MariaDB - Floristería

Este es un proyecto API desarrollado con FastAPI que utiliza MariaDB como base de datos para una floristería.

## Estructura del Proyecto

```
mariadb-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── entidad.py
│   │   ├── carrito.py
│   │   ├── carritodetalle.py
│   │   ├── producto.py
│   │   ├── inventario.py
│   │   ├── compra.py
│   │   ├── compradetalle.py
│   │   ├── compraabono.py
│   │   ├── pedido.py
│   │   ├── pedidodetalle.py
│   │   ├── pedidopago.py
│   │   ├── pedidoenvio.py
│   │   ├── pedidocupon.py
│   │   └── productoensamble.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   ├── entidad.py
│   │   ├── carrito.py
│   │   ├── carritodetalle.py
│   │   ├── producto.py
│   │   ├── inventario.py
│   │   ├── compra.py
│   │   ├── compradetalle.py
│   │   ├── compraabono.py
│   │   ├── pedido.py
│   │   ├── pedidodetalle.py
│   │   ├── pedidopago.py
│   │   ├── pedidoenvio.py
│   │   ├── pedidocupon.py
│   │   └── productoensamble.py
│   └── endpoints/
│       ├── __init__.py
│       ├── entidades.py
│       ├── productos.py
│       ├── pedidos.py
│       ├── carritos.py
│       ├── carritodetalles.py
│       ├── inventarios.py
│       ├── compras.py
│       ├── compradetalles.py
│       ├── compraabonos.py
│       ├── pedidodetalles.py
│       ├── pedidopagos.py
│       ├── pedidoenvios.py
│       ├── pedidocupones.py
│       └── productoensambles.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Instalación

1. Clona este repositorio
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   ```bash
   # En Windows
   venv\Scripts\activate

   # En macOS/Linux
   source venv/bin/activate
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configura las variables de entorno en el archivo `.env`

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=floristeria
SECRET_KEY=clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Iniciar la Aplicación

### Opción 1: Ejecutar localmente
```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Opción 2: Ejecutar con Docker (recomendado)

1. Asegúrate de tener Docker y Docker Compose instalados
2. Desde el directorio raíz del proyecto, ejecuta:

```bash
docker-compose up -d
```

Esto iniciará ambos contenedores (la base de datos MariaDB y la aplicación FastAPI). La API estará disponible en `http://localhost:8000`

Para detener los contenedores:
```bash
docker-compose down
```

Para reconstruir los contenedores después de cambios:
```bash
docker-compose up -d --build
```

## Endpoints Disponibles

- `/api/entidades/` - Gestión de entidades (clientes/proveedores)
- `/api/productos/` - Gestión de productos
- `/api/pedidos/` - Gestión de pedidos
- `/api/carritos/` - Gestión de carritos de compras
- `/api/carritodetalles/` - Gestión de detalles de carritos
- `/api/inventarios/` - Gestión de inventarios
- `/api/compras/` - Gestión de compras a proveedores
- `/api/compradetalles/` - Gestión de detalles de compras
- `/api/compraabonos/` - Gestión de abonos a compras
- `/api/pedidodetalles/` - Gestión de detalles de pedidos
- `/api/pedidopagos/` - Gestión de pagos de pedidos
- `/api/pedidoenvios/` - Gestión de métodos de envío
- `/api/pedidocupones/` - Gestión de cupones de descuento
- `/api/productoensambles/` - Gestión de ensambles de productos

## Documentación de la API

- Documentación interactiva en `http://localhost:8000/docs`
- Documentación alternativa en `http://localhost:8000/redoc`

## Tablas de la Base de Datos

El proyecto incluye modelos y esquemas para las siguientes tablas:

- `entidad` - Información de clientes y proveedores
- `producto` - Catálogo de productos
- `pedido` - Pedidos de clientes
- `carrito` - Carritos de compras
- `inventario` - Inventario de productos
- `compra` - Compras a proveedores
- `carritoDetalle` - Detalles de los carritos
- `compraDetalle` - Detalles de las compras
- `compraAbono` - Abonos a las compras
- `pedidoDetalle` - Detalles de los pedidos
- `pedidoPago` - Pagos de los pedidos
- `pedidoEnvio` - Métodos de envío
- `pedidoCupon` - Cupones de descuento
- `productoEnsamble` - Relación de productos en ensambles