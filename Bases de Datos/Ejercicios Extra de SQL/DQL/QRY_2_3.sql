-- Seleccione productos cuyo product_name contenga la palabra “apple” usando LIKE
select * from products where name like '%apple%';

-- Como no tengo productos con la palabra apple, se hizo con "an"
select * from products where name like '%an%';