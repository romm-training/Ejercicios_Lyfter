-- Obtenga todos los libros y sus autores (en caso de tenerlos)

select b.name as Titulo, a.name as Autor 
from books b 
    left join authors a 
        on b.author = a.id;

