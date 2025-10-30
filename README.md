# API de Floristería con FastAPI y MariaDB

Una API REST moderna y escalable para la gestión completa de una floristería, construida con FastAPI y MariaDB. La aplicación implementa una arquitectura modular con separación clara de responsabilidades y mejores prácticas de desarrollo.

## 🏗️ Arquitectura del Proyecto

```
flower-shop-back/
├── app/
│   ├── main.py                    # Aplicación principal FastAPI
│   ├── database.py                # Configuración de base de datos
│   ├── models/                    # Modelos de base de datos (SQLAlchemy)
│   │   ├── __init__.py           # Exports de modelos
│   │   └── models.py             # Definiciones de modelos
│   ├── schemas/                   # Esquemas Pydantic (serialización)
│   │   ├── categoria.py
│   │   ├── producto.py
│   │   ├── cliente.py
│   │   ├── inventario.py
│   │   ├── cupon.py
│   │   ├── metodoenvio.py
│   │   ├── sede.py
│   │   ├── entidad.py
│   │   ├── carritocompras.py
│   │   ├── pedidos.py
│   │   ├── itemspedido.py
│   │   ├── pagos.py
│   │   ├── compras.py
│   │   └── detallescompra.py
│   └── endpoints/                 # Routers de endpoints
│       ├── categorias.py
│       ├── productos.py
│       ├── clientes.py
│       ├── inventario.py
│       ├── cupones.py
│       ├── metodos_envio.py
│       ├── sedes.py
│       └── entidades.py
├── Dockerfile                     # Instrucciones para construir el contenedor
├── docker-compose.yml             # Configuración multi-contenedor
├── init.sql                       # Script de inicialización de BD
├── datos.sql                      # Datos de ejemplo
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

## ✨ Funcionalidades

La API implementa un sistema completo de gestión para floristería con las siguientes funcionalidades:

### 🛍️ Gestión de Productos
- **Categorías**: Organización de productos por categorías
- **Productos**: Catálogo completo con precios, descripciones e imágenes
- **Inventario**: Control de stock con cantidades mínimas y actualizaciones automáticas

### 👥 Gestión de Clientes
- **Clientes**: Registro y gestión de información de contacto
- **Carrito de compras**: Funcionalidad completa de carrito
- **Pedidos**: Procesamiento completo de pedidos con estados

### 💰 Sistema de Pagos y Envíos
- **Métodos de envío**: Múltiples opciones con costos y tiempos estimados
- **Cupones**: Sistema de descuentos por porcentaje o monto fijo
- **Pagos**: Procesamiento de pagos con múltiples pasarelas

### 🏢 Gestión Empresarial
- **Sedes**: Gestión de múltiples ubicaciones
- **Entidades**: Manejo de clientes y proveedores
- **Compras**: Sistema completo de compras a proveedores

## 🚀 Quick Start

### Prerequisitos
- Docker y Docker Compose instalados
- Python 3.9+ (para desarrollo local)

### Con Docker (Recomendado)
```bash
# Clonar el repositorio
git clone <repository-url>
cd flower-shop-back

# Iniciar los servicios
docker-compose up -d

# Verificar que los servicios estén corriendo
docker-compose ps
```

### Con nerdctl (Alternativa a Docker)
```bash
# Usando nerdctl compose como alternativa
nerdctl compose -f docker-compose.yml up -d

# Verificar contenedores
nerdctl ps
```

### Desarrollo Local
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Acceso a la Aplicación
- **API**: `http://localhost:8000`
- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 📡 API Endpoints

### 🏠 General
- `GET /` - Página principal
- `GET /health` - Health check del servicio
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc

### 📦 Gestión de Productos
- `GET /categorias` - Listar categorías
- `POST /categorias` - Crear categoría
- `GET /productos` - Listar productos (con paginación)
- `POST /productos` - Crear producto
- `GET /inventario` - Consultar inventario
- `POST /inventario` - Actualizar inventario

### 👥 Gestión de Clientes
- `GET /clientes` - Listar clientes
- `POST /clientes` - Registrar cliente

### 🎫 Promociones y Envíos
- `GET /cupones` - Listar cupones
- `POST /cupones` - Crear cupón
- `GET /metodos-envio` - Listar métodos de envío
- `POST /metodos-envio` - Crear método de envío

### 🏢 Gestión Empresarial
- `GET /sedes` - Listar sedes
- `POST /sedes` - Crear sede
- `GET /entidades` - Listar entidades (clientes/proveedores)
- `POST /entidades` - Crear entidad

### 📄 Parámetros de Consulta
Todos los endpoints GET soportan paginación:
- `skip`: Número de registros a omitir (default: 0)
- `limit`: Número máximo de registros (default: 100)

**Ejemplo**: `GET /productos?skip=0&limit=20`

## 🗄️ Esquema de Base de Datos

### Tablas Principales

#### 📦 **Gestión de Productos**
- `categorias` - Categorías de productos
- `productos` - Catálogo de productos con precios e información
- `inventario` - Control de stock y cantidades

#### 👥 **Gestión de Clientes**
- `clientes` - Registro de clientes
- `carritoCompras` - Items en carritos de compra
- `pedidos` - Órdenes de compra
- `itemsPedido` - Detalles de items por pedido

#### 💰 **Sistema de Pagos**
- `pagos` - Transacciones y métodos de pago
- `cupones` - Cupones de descuento
- `metodosEnvio` - Opciones de envío

#### 🏢 **Gestión Empresarial**
- `sedes` - Ubicaciones de la empresa
- `entidades` - Proveedores y clientes corporativos
- `compras` - Órdenes de compra a proveedores
- `detallesCompra` - Detalles de compras

### Características de la BD
- **Motor**: MariaDB 11.4
- **Puerto**: 3307 (para evitar conflictos)
- **Charset**: UTF-8
- **Inicialización**: Automática con `init.sql`
- **Datos de prueba**: Incluidos en `datos.sql`

## 🛠️ Desarrollo

### Hot Reload
Los archivos están montados como volúmenes, permitiendo desarrollo con hot reload automático.

### Estructura de Código
- **Modelos**: SQLAlchemy ORM en `/app/models/`
- **Esquemas**: Pydantic para validación en `/app/schemas/`
- **Endpoints**: Rutas organizadas por entidad en `/app/endpoints/`
- **Main**: Configuración central en `/app/main.py`

### Agregar Nuevos Endpoints
1. Crear schema en `/app/schemas/nueva_entidad.py`
2. Crear router en `/app/endpoints/nueva_entidad.py`
3. Registrar router en `/app/main.py`

## ⚙️ Variables de Entorno

```bash
# Base de datos
DATABASE_URL=mysql+pymysql://fastapi_user:fastapi_password@db:3306/floristeria
MYSQL_HOST=db
MYSQL_USER=fastapi_user
MYSQL_PASSWORD=fastapi_password
MYSQL_DB=floristeria

# MariaDB (contenedor)
MARIADB_ROOT_PASSWORD=rootpassword
MARIADB_DATABASE=floristeria
MARIADB_USER=fastapi_user
MARIADB_PASSWORD=fastapi_password
```

## 🔧 Comandos Útiles

### Docker Compose
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Ejecutar comandos en el contenedor
docker-compose exec app bash

# Detener servicios
docker-compose down

# Limpiar todo (⚠️ elimina datos)
docker-compose down -v
```

### nerdctl (Alternativa)
```bash
# Equivalentes con nerdctl
nerdctl compose -f docker-compose.yml up -d
nerdctl compose logs -f
nerdctl compose down
```

### Base de Datos
```bash
# Conectar a MariaDB
docker-compose exec db mysql -u fastapi_user -p floristeria

# Backup de BD
docker-compose exec db mysqldump -u root -p floristeria > backup.sql

# Restaurar BD
docker-compose exec -T db mysql -u root -p floristeria < backup.sql
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con coverage
pytest --cov=app

# Linting
flake8 app/
black app/
isort app/
```

## 🚀 Despliegue

### Producción
1. Configurar variables de entorno seguras
2. Usar un servidor ASGI como Gunicorn + Uvicorn
3. Configurar proxy reverso (Nginx)
4. SSL/TLS certificates
5. Monitoring y logging

### Docker en Producción
```dockerfile
# Ejemplo de Dockerfile optimizado para producción
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
```

## 🏗️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos y schemas
- **Uvicorn** - Servidor ASGI

### Base de Datos
- **MariaDB 11.4** - Sistema de gestión de base de datos
- **PyMySQL** - Conector Python para MySQL/MariaDB

### Contenedores
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación multi-contenedor
- **nerdctl** - Alternativa compatible con Docker

### Desarrollo
- **Hot Reload** - Desarrollo en tiempo real
- **Swagger UI** - Documentación interactiva
- **ReDoc** - Documentación alternativa

## 📁 Modelos de Datos

### Ejemplo de Producto
```json
{
  "id": 1,
  "nombre": "Ramo de Rosas Rojas",
  "descripcion": "Hermoso ramo de 12 rosas rojas frescas",
  "precio": 45.99,
  "categoriaId": 1,
  "imagenUrl": "https://example.com/rosas-rojas.jpg"
}
```

### Ejemplo de Cliente
```json
{
  "id": 1,
  "nombre": "María",
  "apellido": "González",
  "email": "maria@email.com",
  "telefono": "+1234567890",
  "direccion": "Av. Principal 123, Ciudad"
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte y preguntas:
- Crear un issue en GitHub
- Email: [tu-email@ejemplo.com]

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!