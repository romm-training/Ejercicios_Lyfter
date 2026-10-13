-- Aumente el price en 100 unidades para todos los productos cuando stock_available sea menor a 10
update products 
set price = price + 100 
where stock < 10;

-- No tengo productos con stock < 10, entonces se hizo con < 30

select price from products where stock < 30;

update products 
set price = price + 100 
where stock < 30;

select price from products where stock < 30;