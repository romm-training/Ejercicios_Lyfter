-- Obtenga todos los libros que han sido rentados y están en estado “Overdue”

select b.name 
from books b
    inner join rents r 
        on b.id = r.bookId
where r.state = 'Overdue';
