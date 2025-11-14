-- Archivo de inicialización de la base de datos
CREATE DATABASE IF NOT EXISTS floristeria;
USE floristeria;

-- Tabla de entidades (clientes/proveedores)
CREATE TABLE `entidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nit` varchar(10) NOT NULL,
  `dv` tinyint DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `telefono` varchar(10) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `estado` tinyint DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit_UNIQUE` (`nit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de carrito de compras
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idEntidad` int DEFAULT NULL,
  `sessionToken` varchar(100) NOT NULL,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idEntidad` (`idEntidad`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`idEntidad`) REFERENCES `entidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de detalles del carrito
CREATE TABLE `carritoDetalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCarrito` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precioUnitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idCarrito` (`idCarrito`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `carritodetalle_ibfk_1` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`id`),
  CONSTRAINT `carritodetalle_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de compras a proveedores
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idEntidad` int NOT NULL,
  `factura` varchar(50) DEFAULT NULL,
  `subTotal` decimal(15,2) NOT NULL,
  `descuento` decimal(15,2) DEFAULT '0.00',
  `total` decimal(15,2) NOT NULL,
  `saldo` decimal(15,2) DEFAULT '0.00',
  `metodoPago` varchar(15) DEFAULT 'DE CONTADO',
  `fechaLimite` date DEFAULT NULL,
  `efectivo` decimal(12,2) DEFAULT NULL,
  `transferencia` decimal(12,2) DEFAULT NULL,
  `observacion` varchar(100) DEFAULT NULL,
  `usuario` varchar(10) DEFAULT NULL,
  `registro` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idEntidad` (`idEntidad`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`idEntidad`) REFERENCES `entidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de detalles de compras
CREATE TABLE `compraDetalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCompra` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `iva` int DEFAULT '0',
  `costoIva` decimal(10,2) NOT NULL,
  `totalUnitario` decimal(15,2) DEFAULT NULL,
  `precioVenta` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idCompra` (`idCompra`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `compradetalle_ibfk_1` FOREIGN KEY (`idCompra`) REFERENCES `compra` (`id`),
  CONSTRAINT `compradetalle_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de abonos a compras
CREATE TABLE `compraAbono` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCompra` int NOT NULL,
  `valor` decimal(32,2) NOT NULL,
  `opcionPago` enum('efectivo','trasnferencia') DEFAULT 'efectivo',
  `registro` datetime NOT NULL,
  `usuario` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idCompra` (`idCompra`),
  CONSTRAINT `compraabono_ibfk_1` FOREIGN KEY (`idCompra`) REFERENCES `compra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de pedidos de clientes
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numeroFactura` int DEFAULT NULL,
  `idEntidad` int NOT NULL,
  `subTotal` decimal(15,2) NOT NULL,
  `descuento` decimal(15,2) DEFAULT NULL,
  `montoTotal` decimal(10,2) NOT NULL,
  `saldo` decimal(15,2) DEFAULT NULL,
  `estadoPedido` enum('pendiente','procesando','enviado','entregado','cancelado') DEFAULT 'pendiente',
  `estadoPago` enum('pendiente','pagado','fallido','reembolsado') DEFAULT 'pendiente',
  `metodoPago` varchar(15) DEFAULT 'DE CONTADO',
  `direccionEnvio` text,
  `idCupon` int DEFAULT NULL,
  `idEnvio` int DEFAULT NULL,
  `efectivo` int DEFAULT NULL,
  `transferencia` int DEFAULT NULL,
  `usuario` varchar(10) DEFAULT NULL,
  `registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idEntidad` (`idEntidad`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idEntidad`) REFERENCES `entidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de detalles de pedidos
CREATE TABLE `pedidoDetalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idPedido` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precioUnitario` decimal(10,2) NOT NULL,
  `resigstro` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idPedido` (`idPedido`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `pedidodetalle_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`id`),
  CONSTRAINT `pedidodetalle_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de pagos de pedidos
CREATE TABLE `pedidoPago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idPedido` int NOT NULL,
  `pasarelaPagoId` varchar(255) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `estadoPago` enum('pendiente','completado','fallido','reembolsado') DEFAULT 'pendiente',
  `opcionPago` enum('efectivo','trasnferencia') DEFAULT 'efectivo',
  `idTransaccion` varchar(255) DEFAULT NULL,
  `usuario` varchar(15) DEFAULT NULL,
  `registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idPedido` (`idPedido`),
  CONSTRAINT `pedidopago_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de métodos de envío
CREATE TABLE `pedidoEnvio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `costo` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tiempoEstimadoEntrega` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de cupones de descuento
CREATE TABLE `pedidoCupon` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `tipoDescuento` enum('porcentaje','monto_fijo') NOT NULL,
  `valorDescuento` decimal(10,2) NOT NULL,
  `validoDesde` date DEFAULT NULL,
  `validoHasta` date DEFAULT NULL,
  `limiteUso` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de productos
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) DEFAULT NULL,
  `precioVenta` int DEFAULT NULL,
  `tipo` varchar(45) DEFAULT 'SIMPLE',
  `categoria` varchar(20) NOT NULL,
  `codbarra` varchar(250) DEFAULT NULL,
  `estado` char(2) DEFAULT NULL,
  `descripcion` text,
  `imagenUrl` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de ensambles de productos
CREATE TABLE `productoEnsamble` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idProductoPadre` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `idProductoHijo` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idProductoPadre` (`idProductoPadre`),
  KEY `idProductoHijo` (`idProductoHijo`),
  CONSTRAINT `productoensamble_ibfk_1` FOREIGN KEY (`idProductoPadre`) REFERENCES `producto` (`id`),
  CONSTRAINT `productoensamble_ibfk_2` FOREIGN KEY (`idProductoHijo`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Tabla de inventario
CREATE TABLE `inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idProducto` int DEFAULT NULL,
  `stock` decimal(12,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insertar datos iniciales en la tabla entidad
INSERT INTO entidad (nit, dv, nombre, telefono, correo, estado, direccion) VALUES
('800123456', 7, 'Juan Pérez', '3001234567', 'juan@cliente.com', 1, 'Calle 123 #45-67'),
('900789012', 1, 'Florería ABC', '3107890123', 'info@floreriaabc.com', 1, 'Avenida 45 #78-90'),
('860456123', 5, 'María González', '3204561234', 'maria@cliente.com', 1, 'Carrera 67 #23-45'),
('830987654', 3, 'Distribuciones Flores Ltda', '3119876543', 'contacto@distribuidor.com', 1, 'Calle 100 #50-25');