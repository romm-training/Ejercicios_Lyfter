-- Disminuya stock_available en 1 para un product_id específico

select stock from products where id = 1;

update products 
set stock = stock - 1 
where id = 1;

select stock from products where id = 1;