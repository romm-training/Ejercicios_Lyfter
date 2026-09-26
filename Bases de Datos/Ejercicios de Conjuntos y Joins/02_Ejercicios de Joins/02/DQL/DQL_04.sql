-- Obtenga todos los libros que han sido rentados en algún momento

select b.name 
from books b 
    inner join rents r 
        on b.id = r.bookId
group by b.name;