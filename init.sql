CREATE DATABASE IF NOT EXISTS floristeria;
USE floristeria;

-- Tabla de categorías
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    categoriaId INT,
    imagenUrl VARCHAR(500),
    creadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoriaId) REFERENCES categorias(id)
);

-- Tabla de inventario
CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    productoId INT,
    cantidadStock INT NOT NULL,
    cantidadMinima INT DEFAULT 0,
    ultimaActualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- Tabla de clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    creadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carrito de compras
CREATE TABLE carritoCompras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clienteId INT,
    productoId INT,
    cantidad INT NOT NULL DEFAULT 1,
    agregadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clienteId) REFERENCES clientes(id),
    FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- Tabla de métodos de envío
CREATE TABLE metodosEnvio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL DEFAULT 0,
    tiempoEstimadoEntrega INT -- en días
);

-- Tabla de cupones
CREATE TABLE cupones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    tipoDescuento ENUM('porcentaje', 'monto_fijo') NOT NULL,
    valorDescuento DECIMAL(10, 2) NOT NULL,
    validoDesde DATE,
    validoHasta DATE,
    limiteUso INT DEFAULT NULL
);

-- Tabla de pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clienteId INT,
    montoTotal DECIMAL(10, 2) NOT NULL,
    estadoPedido ENUM('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    estadoPago ENUM('pendiente', 'pagado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    metodoPago VARCHAR(50),
    direccionEnvio TEXT,
    fechaEnvio TIMESTAMP NOT NULL,
    cuponId INT DEFAULT NULL,
    metodoEnvioId INT,
    creadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clienteId) REFERENCES clientes(id),
    FOREIGN KEY (cuponId) REFERENCES cupones(id),
    FOREIGN KEY (metodoEnvioId) REFERENCES metodosEnvio(id)
);

-- Tabla de items de pedido
CREATE TABLE itemsPedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedidoId INT,
    productoId INT,
    cantidad INT NOT NULL,
    precioUnitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedidoId) REFERENCES pedidos(id),
    FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- Tabla de pagos
CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedidoId INT,
    pasarelaPagoId VARCHAR(255) NOT NULL, -- ID de la transacción en la pasarela
    monto DECIMAL(10, 2) NOT NULL,
    estadoPago ENUM('pendiente', 'completado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    metodoPago VARCHAR(50),
    transaccionId VARCHAR(255),
    creadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedidoId) REFERENCES pedidos(id)
);

-- ==============================
-- TABLAS ADICIONALES DESDE datos.sql
-- ==============================

-- Tabla de sedes
CREATE TABLE sedes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20)
);

-- Tabla de entidades (clientes y proveedores)
CREATE TABLE entidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipoEntidad ENUM('cliente', 'proveedor') NOT NULL,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    contacto VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255),
    direccion TEXT
);

-- Tabla de compras
CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idProveedor INT,
    idSede INT,
    total DECIMAL(10, 2) NOT NULL,
    estadoCompra ENUM('pendiente', 'recibida', 'cancelada') DEFAULT 'pendiente',
    creadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idProveedor) REFERENCES entidades(id),
    FOREIGN KEY (idSede) REFERENCES sedes(id)
);

-- Tabla de detalles de compra
CREATE TABLE detallesCompra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idCompra INT,
    productoId INT,
    cantidad INT NOT NULL,
    precioUnitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (idCompra) REFERENCES compras(id),
    FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ==============================
-- INSERTAR DATOS
-- ==============================

-- CATEGORÍAS
INSERT INTO categorias (nombre, descripcion) VALUES
('Rosas', 'Rosas de diferentes colores y tamaños'),
('Tulipanes', 'Tulipanes frescos de temporada'),
('Orquídeas', 'Variedades exóticas de orquídeas'),
('Arreglos', 'Ramos y arreglos florales personalizados');

-- PRODUCTOS
INSERT INTO productos (nombre, descripcion, precio, categoriaId, imagenUrl) VALUES
('Rosa Roja Premium', 'Rosa roja importada, tallo largo.', 55.00, 1, 'rosaroja.jpg'),
('Ramo de Rosas', '12 rosas rojas con envoltura y moño.', 450.00, 4, 'ramo_rosas.jpg'),
('Tulipán Amarillo', 'Tulipán de color amarillo intenso.', 72.00, 2, 'tulipan_amarillo.jpg'),
('Orquídea Blanca', 'Orquídea phalaenopsis blanca.', 650.00, 3, 'orquidea_blanca.jpg'),
('Centro de Mesa Floral', 'Arreglo para eventos y recepciones.', 1200.00, 4, 'centro_mesa.jpg');

-- SEDES
INSERT INTO sedes (nombre, direccion, telefono) VALUES
('Floristería Central', 'Cra 15 #45-20, Bogotá', '3105557788'),
('Floristería Norte', 'Calle 100 #12-34, Bogotá', '3114449966');

-- ENTIDADES (CLIENTES Y PROVEEDORES)
INSERT INTO entidades (tipoEntidad, nombre, apellido, contacto, telefono, email, direccion) VALUES
('cliente', 'Laura', 'Gómez', 'Laura Gómez', '3001234567', 'laura@example.com', 'Calle 45 #10-20'),
('cliente', 'Carlos', 'Rincón', 'Carlos Rincón', '3019876543', 'carlos@example.com', 'Av. 68 #22-15'),
('proveedor', 'Flores del Sol', NULL, 'Jorge Ruiz', '3107779999', 'proveedor1@floressol.com', 'Via a La Vega, KM 5'),
('proveedor', 'Importaciones Verdes', NULL, 'Ana Morales', '3208881122', 'importaciones@verdes.com', 'Calle 100 #5-10');

-- INVENTARIO
INSERT INTO inventario (productoId, cantidadStock, cantidadMinima) VALUES
(1, 200, 50),
(2, 30, 5),
(3, 150, 20),
(4, 25, 5),
(5, 10, 2);

-- COMPRAS
INSERT INTO compras (idProveedor, idSede, total, estadoCompra) VALUES
(3, 1, 2500.00, 'recibida'),
(4, 2, 1800.00, 'pendiente');

INSERT INTO detallesCompra (idCompra, productoId, cantidad, precioUnitario, subtotal) VALUES
(1, 1, 100, 25.00, 2500.00),
(1, 3, 50, 40.00, 2000.00),
(2, 4, 10, 120.00, 1200.00);

-- CUPONES
INSERT INTO cupones (codigo, tipoDescuento, valorDescuento, validoDesde, validoHasta, limiteUso) VALUES
('FLOR10', 'porcentaje', 10, '2025-01-01', '2025-12-31', 100),
('BIENVENIDA', 'monto_fijo', 50.00, '2025-01-01', '2025-06-30', 50);

-- MÉTODOS DE ENVÍO
INSERT INTO metodosEnvio (nombre, costo, tiempoEstimadoEntrega) VALUES
('Entrega estándar', 80.00, 2),
('Entrega express', 150.00, 1),
('Recogida en tienda', 0.00, 0);

-- CLIENTES (creados a partir de entidades tipo cliente)
INSERT INTO clientes (nombre, apellido, email, telefono, direccion) VALUES
('Laura', 'Gómez', 'laura@example.com', '3001234567', 'Calle 45 #10-20'),
('Carlos', 'Rincón', 'carlos@example.com', '3019876543', 'Av. 68 #22-15');

-- PEDIDOS
INSERT INTO pedidos (clienteId, montoTotal, estadoPedido, estadoPago, metodoPago, direccionEnvio, cuponId, metodoEnvioId, fechaEnvio) VALUES
(1, 530.00, 'pendiente', 'pendiente', 'tarjeta', 'Calle 45 #10-20', 1, 2, '2025-11-10 10:00:00'),
(2, 1500.00, 'procesando', 'pagado', 'efectivo', 'Av. 68 #22-15', NULL, 1, '2025-11-08 14:30:00');

INSERT INTO itemsPedido (pedidoId, productoId, cantidad, precioUnitario, subtotal) VALUES
(1, 1, 5, 55.00, 275.00),
(1, 2, 1, 450.00, 450.00),
(2, 4, 2, 650.00, 1300.00);

-- PAGOS
INSERT INTO pagos (pedidoId, pasarelaPagoId, monto, estadoPago, metodoPago, transaccionId) VALUES
(1, 'PAY123', 530.00, 'pendiente', 'tarjeta', 'TXN-9876'),
(2, 'PAY124', 1500.00, 'completado', 'efectivo', 'TXN-6543');