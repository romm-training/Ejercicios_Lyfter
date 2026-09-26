-- Obtenga todos los autores que no tienen libros

select a.name 
from authors a 
    left join books b 
        on a.id = b.author 
where b.id is null;
