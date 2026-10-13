-- Ejercicio 2: Transacción de Compra
-- Construya una transacción para el proceso de compra de múltiples productos. El bloque debe realizar las siguientes validaciones y acciones:
--   Comprobar si hay existencias suficientes de cada uno de los productos dentro de la factura.
--   Confirmar que el usuario que realiza la compra existe en la DB.
--   Insertar la factura con el usuario relacionado.
--   Reducir el stock de los productos según la cantidad comprada.

DO $$

DECLARE 
    v_billid INT; -- Guarda el identificador de la tabla bill.
    v_bill_number INT := 1005; -- El número de la factura a insertar. Valor 1000.
    v_userId INT := 3; --  el identificador del usuario.
    v_stock INT := 0; -- Almacena el stock del producto.
    v_price NUMERIC(18,2) := 0; -- Almacena el precio del producto.
    v_subtotal NUMERIC(18,2) := 0; -- Almacena el subtotal y, en este caso, es el mismo total de la linea.
    v_total NUMERIC(18,2) := 0; -- Acumula el total de los detalles para actualizar el total de la factura.
    rec RECORD; -- Almacena los datos que se van a insertar en la tabla detalle.
BEGIN
    PERFORM set_config('search_path', 'Ejercicio1', True); -- Cambia el esquema de búsqueda a Ejercicio1.

    -- Validar que el usuario existe antes de insertar en la tabla Bill
    IF NOT EXISTS (SELECT 1 
                   FROM "Ejercicio1"."Users"
                   WHERE id = v_userId) THEN
        RAISE EXCEPTION 'El usuario con id % no existe. No se puede insertar en la tabla Bill.', v_userId;
    END IF;

    -- Validar que el numero de factura no exista antes de insertar en la tabla Bill
    IF EXISTS (SELECT 1 
               FROM "Ejercicio1"."Bill"
               WHERE number = v_bill_number) THEN
        RAISE EXCEPTION 'El número de factura % ya existe. No se puede insertar en la tabla Bill.', v_bill_number;
    END IF;

	RAISE NOTICE 'Antes insertar Bill';

    -- Insertar en Bill
    INSERT INTO "Ejercicio1"."Bill" (number, date, "userId", "totalAmount", status)
    VALUES (v_bill_number, now(), v_userId, 0.00, 'Creada')
    RETURNING id INTO v_billid; -- Obtener el id generado para la factura.

	RAISE NOTICE 'Antes insertar BillDetail';
	
    -- Recorrer los datos de prueba
    FOR rec IN 
        SELECT * FROM (VALUES 
            (1, 1), 
            (2, 1)
        ) AS bd(productId, quantity) 
    LOOP
        -- Validar que el producto existe
        IF NOT EXISTS (SELECT 1 
                       FROM "Ejercicio1"."Products" 
                       WHERE id = rec.productId) THEN
            RAISE EXCEPTION 'El producto con id % no existe.', rec.productId;
        END IF;

        -- Obtener el stock y precio del producto
        SELECT stock, price INTO v_stock, v_price
        FROM "Ejercicio1"."Products" 
        WHERE id = rec.productId;

        -- Validar que el stock sea suficiente
        IF v_stock IS NULL OR v_stock < 1 OR v_stock < rec.quantity THEN
            RAISE EXCEPTION 'El producto con id % no tiene suficiente stock.', rec.productId;
        END IF;

        v_subtotal = v_price * rec.quantity;

        -- Insertar en BillDetail
        INSERT INTO "Ejercicio1"."BillDetail" ("productId", quantity, price, subtotal, total, "billId")
        VALUES (rec.productId, rec.quantity, v_price, v_subtotal, v_subtotal, v_billid);

        v_total = v_total + v_subtotal;

        -- Rebajar el stock del producto
        UPDATE "Ejercicio1"."Products"
        SET stock = stock - rec.quantity
        WHERE id = rec.productId;
    END LOOP;

    -- Actualiza el total de factura en la tabla Bill
    UPDATE "Ejercicio1"."Bill"
    SET "totalAmount" = v_total
    WHERE id = v_billid;

	RAISE NOTICE 'Transacción completada exitosamente. Factura insertada con id: %', v_billid;

EXCEPTION 
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM; -- Mostrar el mensaje de error.

END

$$