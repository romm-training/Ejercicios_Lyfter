-- Obtenga todos los libros que no tienen autor

select b.name as Titulo
from books b 
    left join authors a 
        on b.author = a.id
where a.id is null;