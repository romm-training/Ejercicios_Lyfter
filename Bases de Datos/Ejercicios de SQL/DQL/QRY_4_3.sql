-- Obtenga todas las compras de un mismo producto por id.
select * 
from Invoices i 
    inner join ProductsPerInvoice ppi
    on i.id = ppi.invoiceid
where ppi.productid = 2;