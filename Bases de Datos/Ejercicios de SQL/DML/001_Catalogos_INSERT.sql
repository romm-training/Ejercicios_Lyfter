INSERT INTO Users (FullName, Email) VALUES
('Ana Rodríguez', 'ana.rodriguez@mail.com'),
('Carlos Méndez', 'carlos.mendez@mail.com'),
('Laura Jiménez', 'laura.jimenez@mail.com'),
('Diego Vargas', 'diego.vargas@mail.com'),
('María Solano', 'maria.solano@mail.com');

INSERT INTO PaymentMethods (MethodType, BankName) VALUES
('Tarjeta de Crédito', 'BAC Credomatic'),
('Tarjeta de Débito', 'Banco Nacional'),
('Transferencia', 'Banco Popular'),
('Efectivo', NULL),
('SINPE Móvil', 'BCR');

INSERT INTO Products (Code, Name, Price, Brand, Stock) VALUES
('P001', 'Laptop 14"', 549990.00, 'Lenovo', 15),
('P002', 'Mouse Inalámbrico', 12990.00, 'Logitech', 80),
('P003', 'Teclado Mecánico', 34990.00, 'Redragon', 40),
('P004', 'Monitor 24"', 129990.00, 'Samsung', 25),
('P005', 'Audífonos Bluetooth', 24990.00, 'Sony', 60);
