-- Productos
INSERT INTO "Ejercicio1"."Products" (name, stock, price) VALUES
('Laptop X', 10, 500.00),
('Mouse Y', 50, 25.00),
('Keyboard Z', 30, 100.00);

-- Usuarios
INSERT INTO "Ejercicio1"."Users" (username, password, name) VALUES
('jdoe', '12345', 'John Doe'),
('maria', 'abcde', 'María Pérez');

-- Facturas (Bill)
INSERT INTO "Ejercicio1"."Bill" (number, date, "userId", "totalAmount", "status") VALUES
(1001, '2026-09-25 10:30:00', 1, 500.00, "Creada"),
(1002, '2026-09-25 11:00:00', 2, 150.00, "Creada");

-- Detalle de Facturas (BillDetail)
INSERT INTO "Ejercicio1"."BillDetail" ("productId", quantity, price, subtotal, total, "billId") VALUES
(1, 1, 500.00, 500.00, 500.00, 1),   -- Laptop en factura 1001
(2, 2, 25.00, 50.00, 150.00, 2),     -- 2 Mouse en factura 1002
(3, 1, 100.00, 100.00, 150.00, 2);   -- Keyboard en factura 1002
