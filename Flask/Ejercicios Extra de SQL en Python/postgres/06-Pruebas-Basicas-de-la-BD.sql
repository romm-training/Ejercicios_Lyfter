DO $$
DECLARE 
    v_car_rental_id INT;
    v_car_id INT;
    v_user_id INT;
BEGIN
    -- 1
    INSERT INTO lyfter_car_rental."user" (name, email, username, password, birthdate_at, account_status) 
    VALUES ('Usuario de Prueba', 'usuario.prueba@example.com', 'prueba', 'pass1234', '1990-08-16', 'active')
    RETURNING id INTO v_user_id;

    -- 2
    INSERT INTO lyfter_car_rental.car (make, model, year, status) 
    VALUES ('Toyota', 'Corolla', 2020, 'available')
    RETURNING id INTO v_car_id;

    -- 3
    UPDATE lyfter_car_rental."user" 
    SET account_status = 'inactive' 
    WHERE id = v_user_id;

    -- 4
    UPDATE lyfter_car_rental.car 
    SET status = 'reserved' 
    WHERE id = v_car_id;

    -- 5
    INSERT INTO lyfter_car_rental.car_rental (car_id, user_id, return_date_at, status)
    VALUES (v_car_id, v_user_id, NULL, 'active')
    RETURNING id INTO car_rental_id;

    -- 6
    UPDATE lyfter_car_rental.car 
    SET status = 'available' 
    WHERE id = v_car_id;

    UPDATE lyfter_car_rental.car_rental
    SET status = 'completed'
    WHERE id = car_rental_id;

    -- 7

    UPDATE lyfter_car_rental.car 
    SET status = 'maintenance' 
    WHERE id = v_car_id;

END;
$$;

-- 8
SELECT * FROM lyfter_car_rental.car 
WHERE status = 'available';

SELECT * FROM lyfter_car_rental.car 
WHERE status = 'rented';