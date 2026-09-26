-- Obtenga todos los clientes que nunca han rentado un libro

select c.name 
from customers c
    left join rents r 
        on c.id = r.customerId
where r.customerId is null;