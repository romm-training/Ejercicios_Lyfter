-- Obtenga todos los libros y sus autores (en caso de tenerlos)

select b.name as Titulo, a.name as Autor 
from books b 
    inner join authors a 
        on b.author = a.id;

-- Supuesto: Si un libro no tiene autor, no se mostrará en el resultado.    