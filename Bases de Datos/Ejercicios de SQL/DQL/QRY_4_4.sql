-- Obtenga todas las compras agrupadas por producto, donde se muestre el total comprado entre todas las compras.
select ppi.ProductId, p.Name, sum(ppi.TotalAmount) as TotalComprado
from Invoices i 
    inner join ProductsPerInvoice ppi
        on i.id = ppi.invoiceid
    inner join products p
        on ppi.productid = p.id
group by ppi.ProductId, p.Name;

-- Esta consulta permite confirmar el resultado de la consulta anterior
select ppi.ProductId, p.Name, ppi.TotalAmount
from Invoices i 
    inner join ProductsPerInvoice ppi
        on i.id = ppi.invoiceid
    inner join products p
        on ppi.productid = p.id
order by ppi.ProductId;
