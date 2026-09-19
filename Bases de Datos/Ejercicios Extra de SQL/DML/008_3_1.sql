-- Establezca stock_available = 0 donde price <= 0
update products 
set stock = 0 
where price <=0