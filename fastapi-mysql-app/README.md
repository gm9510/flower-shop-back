# API de Floristería con FastAPI y MariaDB

Este es un contenedor de aplicación usando FastAPI como framework web y MariaDB como base de datos. Implementa una API para la gestión de una floristería con todas las funcionalidades necesarias.

## Proyecto

```
fastapi-mysql-app/
├── app/
│   ├── main.py          # Main FastAPI application
│   ├── database.py      # Database configuration
│   └── models.py        # Database models
├── Dockerfile           # Instructions to build the FastAPI container
├── docker-compose.yml   # Multi-container setup
├── init.sql             # Database initialization script (floristeria schema)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Funcionalidades

La API implementa las siguientes funcionalidades:

- **Categorías**: Gestión de categorías de productos
- **Productos**: Gestión de productos con precios, imágenes y descripciones
- **Clientes**: Gestión de clientes con información de contacto
- **Inventario**: Gestión del stock de productos
- **Pedidos**: Gestión del proceso de pedidos
- **Carrito de compras**: Funcionalidad para el carrito de compras
- **Métodos de envío**: Gestión de diferentes métodos de envío
- **Cupones**: Gestión de cupones y descuentos
- **Pagos**: Gestión del proceso de pagos

## Getting Started

1. Asegúrate de tener Docker y Docker Compose instalados
2. Navega al directorio del proyecto: `cd fastapi-mysql-app`
3. Inicia los contenedores: `docker-compose up -d`
4. La aplicación estará disponible en: `http://localhost:8000`
5. La documentación interactiva estará disponible en: `http://localhost:8000/docs`

## Endpoints de la API

- `GET /` - Página principal
- `GET /categorias` - Obtener todas las categorías
- `POST /categorias` - Crear una nueva categoría
- `GET /productos` - Obtener todos los productos
- `POST /productos` - Crear un nuevo producto
- `GET /clientes` - Obtener todos los clientes
- `POST /clientes` - Crear un nuevo cliente
- `GET /inventario` - Obtener todos los registros de inventario
- `POST /inventario` - Crear un nuevo registro de inventario
- `GET /docs` - Documentación interactiva de la API (Swagger UI)
- `GET /redoc` - Documentación alternativa (ReDoc)
- `GET /health` - Verificar el estado del servicio

## Base de Datos

Se está usando el esquema de la floristería (`floristeria_schema_clean.sql`) que incluye las siguientes tablas:

- `categorias` - Categorías de productos
- `productos` - Información de los productos
- `clientes` - Información de los clientes
- `inventario` - Stock de productos
- `carritoCompras` - Items en el carrito de compras
- `metodosEnvio` - Métodos de envío disponibles
- `cupones` - Cupones y descuentos
- `pedidos` - Pedidos de los clientes
- `itemsPedido` - Items de cada pedido
- `pagos` - Información de los pagos

## Desarrollo

Para desarrollo, los archivos de la aplicación están montados como volúmenes, por lo que los cambios se reflejan inmediatamente en el contenedor.

## Variables de Entorno

La aplicación usa las siguientes variables de entorno (definidas en docker-compose.yml):

- `DATABASE_URL` - Cadena de conexión a la base de datos
- `MYSQL_HOST` - Host de la base de datos
- `MYSQL_USER` - Usuario de la base de datos
- `MYSQL_PASSWORD` - Contraseña de la base de datos
- `MYSQL_DB` - Nombre de la base de datos

## Detener la Aplicación

Para detener los contenedores, presiona `Ctrl+C` en la terminal donde estén corriendo.
Para eliminar los contenedores y volúmenes: `docker-compose down -v`