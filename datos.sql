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
INSERT INTO productos (nombre, descripcion, precio, categoriaId, imagenUrl) VALUES
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
('cliente', 'María', 'Fernández', 'María Fernández', '3002223344', 'maria@example.com', 'Carrera 7 #80-45'),
('cliente', 'Juan', 'Martínez', 'Juan Martínez', '3155556677', 'juan@example.com', 'Calle 127 #15-20'),
('cliente', 'Andrea', 'López', 'Andrea López', '3178889900', 'andrea@example.com', 'Av. El Dorado #50-30'),
('proveedor', 'Flores del Sol', NULL, 'Jorge Ruiz', '3107779999', 'proveedor1@floressol.com', 'Via a La Vega, KM 5'),
('proveedor', 'Importaciones Verdes', NULL, 'Ana Morales', '3208881122', 'importaciones@verdes.com', 'Calle 100 #5-10');

-- ==============================
-- INVENTARIO
-- ==============================
INSERT INTO inventario (productoId, cantidadStock, cantidadMinima) VALUES
(1, 200, 50),
(2, 30, 5),
(3, 150, 20),
(4, 25, 5),
(5, 10, 2);

-- ==============================
-- COMPRAS
-- ==============================
INSERT INTO compras (idProveedor, idSede, total, estadoCompra) VALUES
(3, 1, 250000, 'recibida'),
(4, 2, 180000, 'pendiente');

INSERT INTO detallesCompra (idCompra, productoId, cantidad, precioUnitario, subtotal) VALUES
(1, 1, 100, 2500, 250000),
(1, 3, 50, 4000, 200000),
(2, 4, 10, 12000, 120000);

-- ==============================
-- CLIENTES
-- ==============================
INSERT INTO clientes (nombre, apellido, email, telefono, direccion) VALUES
('Laura', 'Gómez', 'laura@example.com', '3001234567', 'Calle 45 #10-20'),
('Carlos', 'Rincón', 'carlos@example.com', '3019876543', 'Av. 68 #22-15'),
('María', 'Fernández', 'maria@example.com', '3002223344', 'Carrera 7 #80-45'),
('Juan', 'Martínez', 'juan@example.com', '3155556677', 'Calle 127 #15-20'),
('Andrea', 'López', 'andrea@example.com', '3178889900', 'Av. El Dorado #50-30');

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
-- PEDIDOS (Comprehensive test data for all enum combinations)
-- ==============================
-- estadoPedido: 'pendiente', 'procesando', 'enviado', 'entregado', 'cancelado'
-- estadoPago: 'pendiente', 'pagado', 'fallido', 'reembolsado'
INSERT INTO pedidos (clienteId, montoTotal, estadoPedido, estadoPago, metodoPago, direccionEnvio, cuponId, metodoEnvioId, fechaEnvio) VALUES
-- Pedido 1: pendiente + pendiente
(1, 53000, 'pendiente', 'pendiente', 'tarjeta', 'Calle 45 #10-20', 1, 2, '2025-11-10 10:00:00'),
-- Pedido 2: procesando + pagado
(2, 150000, 'procesando', 'pagado', 'efectivo', 'Av. 68 #22-15', NULL, 1, '2025-11-08 14:30:00'),
-- Pedido 3: enviado + pagado
(3, 87000, 'enviado', 'pagado', 'transferencia', 'Carrera 7 #80-45', 2, 2, '2025-11-09 16:00:00'),
-- Pedido 4: entregado + pagado
(1, 72000, 'entregado', 'pagado', 'tarjeta', 'Calle 45 #10-20', NULL, 1, '2025-11-05 09:30:00'),
-- Pedido 5: cancelado + reembolsado
(4, 120000, 'cancelado', 'reembolsado', 'tarjeta', 'Calle 127 #15-20', NULL, 2, '2025-11-13 10:00:00'),
-- Pedido 6: pendiente + pagado
(5, 195000, 'pendiente', 'pagado', 'pse', 'Av. El Dorado #50-30', 1, 1, '2025-11-11 11:00:00'),
-- Pedido 7: procesando + pendiente
(2, 65000, 'procesando', 'pendiente', 'contraentrega', 'Av. 68 #22-15', NULL, 3, '2025-11-12 10:00:00'),
-- Pedido 8: enviado + pendiente (contraentrega)
(3, 45000, 'enviado', 'pendiente', 'contraentrega', 'Carrera 7 #80-45', NULL, 2, '2025-11-08 08:00:00'),
-- Pedido 9: pendiente + fallido
(4, 155000, 'pendiente', 'fallido', 'tarjeta', 'Calle 127 #15-20', NULL, 2, '2025-11-15 14:00:00'),
-- Pedido 10: cancelado + fallido
(5, 98000, 'cancelado', 'fallido', 'tarjeta', 'Av. El Dorado #50-30', NULL, 1, '2025-11-16 09:00:00'),
-- Pedido 11: entregado + reembolsado (devuelto)
(1, 65000, 'entregado', 'reembolsado', 'tarjeta', 'Calle 45 #10-20', NULL, 2, '2025-11-03 15:00:00'),
-- Pedido 12: procesando + fallido (reintento)
(3, 125000, 'procesando', 'fallido', 'pse', 'Carrera 7 #80-45', NULL, 1, '2025-11-14 12:00:00');

INSERT INTO itemsPedido (pedidoId, productoId, cantidad, precioUnitario, subtotal) VALUES
-- Pedido 1
(1, 1, 5, 5500, 27500),
(1, 2, 1, 45000, 45000),
-- Pedido 2
(2, 4, 2, 65000, 130000),
(2, 3, 3, 7200, 21600),
-- Pedido 3
(3, 2, 1, 45000, 45000),
(3, 1, 3, 5500, 16500),
(3, 3, 2, 7200, 14400),
-- Pedido 4
(4, 3, 10, 7200, 72000),
-- Pedido 5
(5, 5, 1, 120000, 120000),
-- Pedido 6
(6, 4, 3, 65000, 195000),
-- Pedido 7
(7, 4, 1, 65000, 65000),
-- Pedido 8
(8, 2, 1, 45000, 45000),
-- Pedido 9
(9, 5, 1, 120000, 120000),
(9, 1, 5, 5500, 27500),
-- Pedido 10
(10, 4, 1, 65000, 65000),
(10, 1, 6, 5500, 33000),
-- Pedido 11
(11, 4, 1, 65000, 65000),
-- Pedido 12
(12, 5, 1, 120000, 120000),
(12, 1, 1, 5500, 5500);

-- ==============================
-- PAGOS (Matching all pedidos with their payment status)
-- ==============================
INSERT INTO pagos (pedidoId, pasarelaPagoId, monto, estadoPago, metodoPago, transaccionId) VALUES
-- Pedido 1: pendiente
(1, 'PAY-001', 53000, 'pendiente', 'tarjeta', 'TXN-001'),
-- Pedido 2: pagado (completado)
(2, 'PAY-002', 150000, 'completado', 'efectivo', 'TXN-002'),
-- Pedido 3: pagado (completado)
(3, 'PAY-003', 87000, 'completado', 'transferencia', 'TXN-003'),
-- Pedido 4: pagado (completado)
(4, 'PAY-004', 72000, 'completado', 'tarjeta', 'TXN-004'),
-- Pedido 5: reembolsado
(5, 'PAY-005', 120000, 'reembolsado', 'tarjeta', 'TXN-005'),
-- Pedido 6: pagado (completado)
(6, 'PAY-006', 195000, 'completado', 'pse', 'TXN-006'),
-- Pedido 7: pendiente (contraentrega)
(7, 'PAY-007', 65000, 'pendiente', 'contraentrega', 'TXN-007'),
-- Pedido 8: pendiente (contraentrega)
(8, 'PAY-008', 45000, 'pendiente', 'contraentrega', 'TXN-008'),
-- Pedido 9: fallido
(9, 'PAY-009', 155000, 'fallido', 'tarjeta', 'TXN-009'),
-- Pedido 10: fallido
(10, 'PAY-010', 98000, 'fallido', 'tarjeta', 'TXN-010'),
-- Pedido 11: reembolsado (producto devuelto)
(11, 'PAY-011', 65000, 'reembolsado', 'tarjeta', 'TXN-011'),
-- Pedido 12: fallido (intento fallido)
(12, 'PAY-012', 125000, 'fallido', 'pse', 'TXN-012');
