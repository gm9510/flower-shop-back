USE floristeria;

-- ==============================
-- ENTIDADES (Clientes y Proveedores)
-- ==============================
INSERT INTO entidad (nit, dv, nombre, telefono, correo, estado, direccion) VALUES
('1234567890', 1, 'Laura Gómez', '3001234567', 'laura@example.com', 1, 'Calle 45 #10-20, Bogotá'),
('9876543210', 2, 'Carlos Rincón', '3019876543', 'carlos@example.com', 1, 'Av. 68 #22-15, Bogotá'),
('5555555555', 5, 'María Fernández', '3002223344', 'maria@example.com', 1, 'Carrera 7 #80-45, Bogotá'),
('7777777777', 7, 'Juan Martínez', '3155556677', 'juan@example.com', 1, 'Calle 127 #15-20, Bogotá'),
('8888888888', 8, 'Andrea López', '3178889900', 'andrea@example.com', 1, 'Av. El Dorado #50-30, Bogotá'),
('9001234567', 9, 'Flores del Sol - Proveedor', '3107779999', 'proveedor1@floressol.com', 1, 'Via a La Vega, KM 5'),
('9009876543', 0, 'Importaciones Verdes - Proveedor', '3208881122', 'importaciones@verdes.com', 1, 'Calle 100 #5-10, Bogotá');

-- ==============================
-- PRODUCTOS
-- ==============================
INSERT INTO producto (nombre, precioVenta, tipo, categoria, codbarra, estado, descripcion, imagenUrl) VALUES
('Rosa Roja Premium', 5500, 'SIMPLE', 'Rosas', '7501234567890', 'AC', 'Rosa roja importada, tallo largo', 'https://example.com/images/rosa_roja.jpg'),
('Ramo de Rosas', 45000, 'ENSAMBLE', 'Arreglos', '7501234567891', 'AC', '12 rosas rojas con envoltura y moño', 'https://example.com/images/ramo_rosas.jpg'),
('Tulipán Amarillo', 7200, 'SIMPLE', 'Tulipanes', '7501234567892', 'AC', 'Tulipán de color amarillo intenso', 'https://example.com/images/tulipan_amarillo.jpg'),
('Orquídea Blanca', 65000, 'SIMPLE', 'Orquídeas', '7501234567893', 'AC', 'Orquídea phalaenopsis blanca', 'https://example.com/images/orquidea_blanca.jpg'),
('Centro de Mesa Floral', 120000, 'ENSAMBLE', 'Arreglos', '7501234567894', 'AC', 'Arreglo para eventos y recepciones', 'https://example.com/images/centro_mesa.jpg'),
('Lirio Blanco', 8500, 'SIMPLE', 'Lirios', '7501234567895', 'AC', 'Lirio blanco aromático', 'https://example.com/images/lirio_blanco.jpg'),
('Girasol Grande', 6800, 'SIMPLE', 'Girasoles', '7501234567896', 'AC', 'Girasol grande y fresco', 'https://example.com/images/girasol.jpg'),
('Ramo Mixto Primavera', 58000, 'ENSAMBLE', 'Arreglos', '7501234567897', 'AC', 'Combinación de flores de temporada', 'https://example.com/images/ramo_mixto.jpg');

-- ==============================
-- INVENTARIO
-- ==============================
INSERT INTO inventario (idProducto, stock) VALUES
(1, 200.00),
(2, 30.00),
(3, 150.00),
(4, 25.00),
(5, 10.00),
(6, 80.00),
(7, 120.00),
(8, 15.00);

-- ==============================
-- PRODUCTO ENSAMBLES (Ramos y arreglos compuestos)
-- ==============================
INSERT INTO productoEnsamble (idProductoPadre, cantidad, idProductoHijo) VALUES
-- Ramo de Rosas (producto 2) compuesto por 12 rosas
(2, 12.00, 1),
-- Centro de Mesa Floral (producto 5) compuesto por varias flores
(5, 5.00, 1),  -- 5 rosas
(5, 3.00, 4),  -- 3 orquídeas
(5, 4.00, 6),  -- 4 lirios
-- Ramo Mixto Primavera (producto 8)
(8, 3.00, 1),  -- 3 rosas
(8, 4.00, 3),  -- 4 tulipanes
(8, 2.00, 7);  -- 2 girasoles

-- ==============================
-- CARRITOS
-- ==============================
INSERT INTO carrito (idEntidad, sessionToken, registro) VALUES
(1, 'session_token_abc123', '2025-11-27 10:00:00'),
(2, 'session_token_def456', '2025-11-27 11:30:00'),
(NULL, 'session_token_guest789', '2025-11-27 12:00:00');

-- ==============================
-- CARRITO DETALLES
-- ==============================
INSERT INTO carritoDetalle (idCarrito, idProducto, cantidad, precioUnitario) VALUES
(1, 1, 5, 5500.00),
(1, 3, 2, 7200.00),
(2, 2, 1, 45000.00),
(2, 4, 1, 65000.00),
(3, 7, 3, 6800.00);

-- ==============================
-- COMPRAS (a proveedores)
-- ==============================
INSERT INTO compra (idEntidad, factura, subTotal, descuento, total, saldo, metodoPago, fechaLimite, efectivo, transferencia, observacion, usuario, registro) VALUES
(6, 'FAC-001', 250000.00, 0.00, 250000.00, 0.00, 'DE CONTADO', NULL, 250000.00, NULL, 'Compra de rosas', 'admin', '2025-11-01 09:00:00'),
(7, 'FAC-002', 180000.00, 10000.00, 170000.00, 85000.00, 'A CREDITO', '2025-12-15', 85000.00, NULL, 'Compra de orquídeas', 'admin', '2025-11-10 14:00:00'),
(6, 'FAC-003', 150000.00, 0.00, 150000.00, 0.00, 'DE CONTADO', NULL, NULL, 150000.00, 'Compra de tulipanes', 'admin', '2025-11-15 10:30:00');

-- ==============================
-- COMPRA DETALLES
-- ==============================
INSERT INTO compraDetalle (idCompra, idProducto, cantidad, costo, iva, costoIva, totalUnitario, precioVenta) VALUES
(1, 1, 100, 2500.00, 19, 2975.00, 2975.00, 5500.00),
(1, 3, 50, 4000.00, 19, 4760.00, 4760.00, 7200.00),
(2, 4, 10, 45000.00, 19, 53550.00, 53550.00, 65000.00),
(2, 6, 15, 4500.00, 19, 5355.00, 5355.00, 8500.00),
(3, 3, 40, 3800.00, 19, 4522.00, 4522.00, 7200.00);

-- ==============================
-- COMPRA ABONOS
-- ==============================
INSERT INTO compraAbono (idCompra, valor, opcionPago, registro, usuario) VALUES
(2, 85000.00, 'efectivo', '2025-11-10 15:00:00', 'admin');

-- ==============================
-- PEDIDO CUPONES
-- ==============================
INSERT INTO pedidoCupon (codigo, tipoDescuento, valorDescuento, validoDesde, validoHasta, limiteUso) VALUES
('FLOR10', 'porcentaje', 10.00, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 100),
('BIENVENIDA', 'monto_fijo', 5000.00, '2025-01-01 00:00:00', '2025-06-30 23:59:59', 50),
('NAVIDAD2025', 'porcentaje', 15.00, '2025-12-01 00:00:00', '2025-12-25 23:59:59', 200);

-- ==============================
-- PEDIDO ENVIOS (métodos de envío)
-- ==============================
INSERT INTO pedidoEnvio (nombre, costo, tiempoEstimadoEntrega) VALUES
('Entrega estándar', 8000.00, 2),
('Entrega express', 15000.00, 1),
('Recogida en tienda', 0.00, 0),
('Entrega mismo día', 25000.00, 0);

-- ==============================
-- PEDIDOS
-- ==============================
INSERT INTO pedido (numeroFactura, idEntidad, subTotal, descuento, montoTotal, saldo, estadoPedido, estadoPago, metodoPago, direccionEnvio, fechaEntrega, idCupon, idEnvio, efectivo, transferencia, usuario, registro) VALUES
-- Pedido 1: pendiente + pendiente
(1001, 1, 50000.00, 5000.00, 45000.00, 45000.00, 'pendiente', 'pendiente', 'DE CONTADO', 'Calle 45 #10-20, Bogotá', '2025-11-29 10:00:00', 1, 2, NULL, NULL, 'user01', '2025-11-27 10:30:00'),
-- Pedido 2: procesando + pagado
(1002, 2, 145000.00, 0.00, 145000.00, 0.00, 'procesando', 'pagado', 'DE CONTADO', 'Av. 68 #22-15, Bogotá', '2025-11-30 14:00:00', NULL, 1, 145000, NULL, 'user02', '2025-11-27 11:00:00'),
-- Pedido 3: enviado + pagado
(1003, 3, 80000.00, 8000.00, 72000.00, 0.00, 'enviado', 'pagado', 'DE CONTADO', 'Carrera 7 #80-45, Bogotá', '2025-11-28 16:00:00', 2, 2, NULL, 72000, 'user03', '2025-11-26 09:00:00'),
-- Pedido 4: entregado + pagado
(1004, 1, 72000.00, 0.00, 72000.00, 0.00, 'entregado', 'pagado', 'DE CONTADO', 'Calle 45 #10-20, Bogotá', '2025-11-25 09:30:00', NULL, 1, 72000, NULL, 'user01', '2025-11-23 08:00:00'),
-- Pedido 5: cancelado + reembolsado
(1005, 4, 120000.00, 0.00, 120000.00, 0.00, 'cancelado', 'reembolsado', 'DE CONTADO', 'Calle 127 #15-20, Bogotá', '2025-12-05 10:00:00', NULL, 2, NULL, NULL, 'user04', '2025-11-27 13:00:00'),
-- Pedido 6: pendiente + pagado
(1006, 5, 195000.00, 0.00, 195000.00, 0.00, 'pendiente', 'pagado', 'DE CONTADO', 'Av. El Dorado #50-30, Bogotá', '2025-11-30 11:00:00', NULL, 1, NULL, 195000, 'user05', '2025-11-27 14:00:00'),
-- Pedido 7: procesando + pendiente
(1007, 2, 65000.00, 0.00, 65000.00, 65000.00, 'procesando', 'pendiente', 'DE CONTADO', 'Av. 68 #22-15, Bogotá', '2025-11-29 10:00:00', NULL, 3, NULL, NULL, 'user02', '2025-11-27 15:00:00'),
-- Pedido 8: enviado + pendiente
(1008, 3, 45000.00, 0.00, 45000.00, 45000.00, 'enviado', 'pendiente', 'DE CONTADO', 'Carrera 7 #80-45, Bogotá', '2025-11-28 08:00:00', NULL, 2, NULL, NULL, 'user03', '2025-11-26 07:00:00'),
-- Pedido 9: pendiente + fallido
(1009, 4, 155000.00, 0.00, 155000.00, 155000.00, 'pendiente', 'fallido', 'DE CONTADO', 'Calle 127 #15-20, Bogotá', '2025-12-01 14:00:00', NULL, 2, NULL, NULL, 'user04', '2025-11-27 16:00:00');

-- ==============================
-- PEDIDO DETALLES
-- ==============================
INSERT INTO pedidoDetalle (idPedido, idProducto, cantidad, precioUnitario, resigstro) VALUES
-- Pedido 1
(1, 1, 5, 5500.00, '2025-11-27 10:30:00'),
(1, 3, 2, 7200.00, '2025-11-27 10:30:00'),
-- Pedido 2
(2, 4, 2, 65000.00, '2025-11-27 11:00:00'),
(2, 3, 2, 7200.00, '2025-11-27 11:00:00'),
-- Pedido 3
(3, 2, 1, 45000.00, '2025-11-26 09:00:00'),
(3, 1, 3, 5500.00, '2025-11-26 09:00:00'),
-- Pedido 4
(4, 3, 10, 7200.00, '2025-11-23 08:00:00'),
-- Pedido 5
(5, 5, 1, 120000.00, '2025-11-27 13:00:00'),
-- Pedido 6
(6, 4, 3, 65000.00, '2025-11-27 14:00:00'),
-- Pedido 7
(7, 4, 1, 65000.00, '2025-11-27 15:00:00'),
-- Pedido 8
(8, 2, 1, 45000.00, '2025-11-26 07:00:00'),
-- Pedido 9
(9, 5, 1, 120000.00, '2025-11-27 16:00:00'),
(9, 1, 5, 5500.00, '2025-11-27 16:00:00');

-- ==============================
-- PEDIDO PAGOS
-- ==============================
INSERT INTO pedidoPago (idPedido, pasarelaPagoId, monto, estadoPago, opcionPago, idTransaccion, usuario, registro) VALUES
-- Pedido 1: pendiente
(1, 'GATEWAY-PAY-001', 45000.00, 'pendiente', 'tarjeta', 'TXN-001', 'user01', '2025-11-27 10:31:00'),
-- Pedido 2: completado (pagado)
(2, 'GATEWAY-PAY-002', 145000.00, 'completado', 'efectivo', 'TXN-002', 'user02', '2025-11-27 11:01:00'),
-- Pedido 3: completado (pagado)
(3, 'GATEWAY-PAY-003', 72000.00, 'completado', 'transferencia', 'TXN-003', 'user03', '2025-11-26 09:01:00'),
-- Pedido 4: completado (pagado)
(4, 'GATEWAY-PAY-004', 72000.00, 'completado', 'efectivo', 'TXN-004', 'user01', '2025-11-23 08:01:00'),
-- Pedido 5: pendiente (será reembolsado)
(5, 'GATEWAY-PAY-005', 120000.00, 'pendiente', 'tarjeta', 'TXN-005', 'user04', '2025-11-27 13:01:00'),
-- Pedido 6: completado (pagado)
(6, 'GATEWAY-PAY-006', 195000.00, 'completado', 'transferencia', 'TXN-006', 'user05', '2025-11-27 14:01:00'),
-- Pedido 7: pendiente
(7, 'GATEWAY-PAY-007', 65000.00, 'pendiente', 'efectivo', 'TXN-007', 'user02', '2025-11-27 15:01:00'),
-- Pedido 8: pendiente
(8, 'GATEWAY-PAY-008', 45000.00, 'pendiente', 'efectivo', 'TXN-008', 'user03', '2025-11-26 07:01:00'),
-- Pedido 9: fallido
(9, 'GATEWAY-PAY-009', 155000.00, 'fallido', 'tarjeta', 'TXN-009', 'user04', '2025-11-27 16:01:00');
