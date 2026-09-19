INSERT INTO Invoices (Number, TotalAmount, UserId, PaymentMethodId, CustomerPhoneNumber, SellerCode) VALUES
(1001, 562980.00, 1, 1, '88881111', 'SEL01'),
(1002, 47980.00, 2, 3, '88882222', 'SEL02'),
(1003, 129990.00, 3, 2, '88883333', 'SEL01'),
(1004, 59980.00, 4, 4, '88884444', 'SEL03'),
(1005, 24990.00, 5, 5, '88885555', 'SEL02');

INSERT INTO ProductsPerInvoice (InvoiceId, ProductId, Quantity, TotalAmount) VALUES
(1, 1, 1, 549990.00),
(1, 2, 1, 12990.00),
(2, 3, 1, 34990.00),
(2, 2, 1, 12990.00),
(3, 4, 1, 129990.00),
(4, 5, 2, 49980.00),
(4, 2, 1, 9990.00),
(5, 5, 1, 24990.00);
