USE floristeria;

-- ==============================
-- CATEGORÍAS
-- ==============================
INSERT INTO categorias (nombre, descripcion) VALUES
('Rosas', 'Rosas de diferentes colores y tamaños'),
('Tulipanes', 'Tulipanes frescos de temporada'),
('Orquídeas', 'Variedades exóticas de orquídeas'),
('Arreglos', 'Ramos y arreglos florales personalizados');

-- ==============================
-- PRODUCTOS
-- ==============================
INSERT INTO productos (nombre, descripcion, precio, idCategoria, imagenUrl) VALUES
('Rosa Roja Premium', 'Rosa roja importada, tallo largo.', 5500, 1, 'rosaroja.jpg'),
('Ramo de Rosas', '12 rosas rojas con envoltura y moño.', 45000, 4, 'ramo_rosas.jpg'),
('Tulipán Amarillo', 'Tulipán de color amarillo intenso.', 7200, 2, 'tulipan_amarillo.jpg'),
('Orquídea Blanca', 'Orquídea phalaenopsis blanca.', 65000, 3, 'orquidea_blanca.jpg'),
('Centro de Mesa Floral', 'Arreglo para eventos y recepciones.', 120000, 4, 'centro_mesa.jpg');

-- ==============================
-- SEDES
-- ==============================
INSERT INTO sedes (nombre, direccion, telefono) VALUES
('Floristería Central', 'Cra 15 #45-20, Bogotá', '3105557788'),
('Floristería Norte', 'Calle 100 #12-34, Bogotá', '3114449966');

-- ==============================
-- ENTIDADES (CLIENTES Y PROVEEDORES)
-- ==============================
INSERT INTO entidades (tipoEntidad, nombre, apellido, contacto, telefono, email, direccion) VALUES
('cliente', 'Laura', 'Gómez', 'Laura Gómez', '3001234567', 'laura@example.com', 'Calle 45 #10-20'),
('cliente', 'Carlos', 'Rincón', 'Carlos Rincón', '3019876543', 'carlos@example.com', 'Av. 68 #22-15'),
('proveedor', 'Flores del Sol', NULL, 'Jorge Ruiz', '3107779999', 'proveedor1@floressol.com', 'Via a La Vega, KM 5'),
('proveedor', 'Importaciones Verdes', NULL, 'Ana Morales', '3208881122', 'importaciones@verdes.com', 'Calle 100 #5-10');

-- ==============================
-- INVENTARIO
-- ==============================
INSERT INTO inventario (idProducto, idSede, stock, stockMinimo) VALUES
(1, 1, 200, 50),
(2, 1, 30, 5),
(3, 1, 150, 20),
(4, 2, 25, 5),
(5, 2, 10, 2);

-- ==============================
-- COMPRAS
-- ==============================
INSERT INTO compras (idProveedor, idSede, total, estadoCompra) VALUES
(3, 1, 250000, 'recibida'),
(4, 2, 180000, 'pendiente');

INSERT INTO detallesCompra (idCompra, idProducto, cantidad, precioUnitario) VALUES
(1, 1, 100, 2500),
(1, 3, 50, 4000),
(2, 4, 10, 12000);

-- ==============================
-- CUPONES
-- ==============================
INSERT INTO cupones (codigo, tipoDescuento, valorDescuento, validoDesde, validoHasta, limiteUso) VALUES
('FLOR10', 'porcentaje', 10, '2025-01-01', '2025-12-31', 100),
('BIENVENIDA', 'monto_fijo', 5000, '2025-01-01', '2025-06-30', 50);

-- ==============================
-- MÉTODOS DE ENVÍO
-- ==============================
INSERT INTO metodosEnvio (nombre, costo, tiempoEstimadoEntrega) VALUES
('Entrega estándar', 8000, 2),
('Entrega express', 15000, 1),
('Recogida en tienda', 0, 0);

-- ==============================
-- PEDIDOS
-- ==============================
INSERT INTO pedidos (idCliente, montoTotal, estadoPedido, estadoPago, metodoPago, direccionEnvio, idCupon, idMetodoEnvio) VALUES
(1, 53000, 'pendiente', 'pendiente', 'tarjeta', 'Calle 45 #10-20', 1, 2),
(2, 150000, 'procesando', 'pagado', 'efectivo', 'Av. 68 #22-15', NULL, 1);

INSERT INTO itemsPedido (idPedido, idProducto, cantidad, precioUnitario) VALUES
(1, 1, 5, 5500),
(1, 2, 1, 45000),
(2, 4, 2, 65000);

-- ==============================
-- PAGOS
-- ==============================
INSERT INTO pagos (idPedido, pasarelaPagoId, monto, estadoPago, metodoPago, idTransaccion) VALUES
(1, 'PAY123', 53000, 'pendiente', 'tarjeta', 'TXN-9876'),
(2, 'PAY124', 150000, 'completado', 'efectivo', 'TXN-6543');
