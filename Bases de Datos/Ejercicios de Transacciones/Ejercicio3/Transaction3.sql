-- Ejercicio 3: Transacción de Retorno de Productos
-- Construya una transacción para procesar la devolución de uno o varios productos. La transacción debe seguir este flujo:
--   Verificar que la factura existe en la base de datos.
--   Aumentar el stock de los productos en la cantidad que se registró en la compra.
--   Modificar la factura original para marcarla con el estado de "Retornada".

DO $$

DECLARE 
	v_billid INT; -- Identificador de la factura.
    v_bill_number INT := 1004; -- El número de la factura a insertar.
    v_userId INT := 3; --  el identificador del usuario.
    rec RECORD; -- Almacena los datos que se van a insertar en la tabla detalle.
BEGIN
    PERFORM set_config('search_path', 'Ejercicio1', True); -- Cambia el esquema de búsqueda a Ejercicio1.

    -- Validar que el numero de factura exista y que no este en estado Retornada, para no retornar dos veces la misma factura.
    SELECT id INTO v_billid 
    FROM "Ejercicio1"."Bill"
    WHERE number = v_bill_number AND status != 'Retornada';

    IF v_billid IS NULL THEN
        RAISE EXCEPTION 'El número de factura % no existe o ya fue retornada.', v_bill_number;
    END IF;

    -- Recorrer los productos de la factura para aumentar el stock
    FOR rec IN 
        SELECT "productId" as productId, quantity 
		FROM "Ejercicio1"."BillDetail"
        WHERE "billId" = v_billid
    LOOP
       -- Aumentar el stock del producto
        UPDATE "Ejercicio1"."Products"
        SET stock = stock + rec.quantity
        WHERE id = rec.productId;
    END LOOP;

    -- Modificar el estado de la factura a "Retornada"
    UPDATE "Ejercicio1"."Bill"
    SET status = 'Retornada'
    WHERE id = v_billid;

	RAISE NOTICE 'Transacción completada exitosamente. Factura retornada con id: %', v_billid;

EXCEPTION 
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM; -- Mostrar el mensaje de error.
        ROLLBACK; -- Deshacer la transacción en caso de error.

END

$$