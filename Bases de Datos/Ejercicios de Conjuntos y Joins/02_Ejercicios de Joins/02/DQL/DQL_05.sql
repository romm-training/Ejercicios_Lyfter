-- Obtenga todos los libros que nunca han sido rentados

select b.name 
from books b 
    left join rents r 
        on b.id = r.bookId
where r.bookId is null;