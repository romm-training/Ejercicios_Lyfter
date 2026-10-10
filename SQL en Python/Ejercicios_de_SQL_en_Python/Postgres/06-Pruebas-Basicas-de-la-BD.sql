INSERT INTO lyfter_car_rental."user" (name, email, username, password, birthdate_at, account_status) 
VALUES ('Usuario de Prueba', 'usuario.prueba@example.com', 'prueba', 'pass1234', '1990-08-16', 'active');

INSERT INTO lyfter_car_rental.car (make, model, year, status) 
VALUES ('Toyota', 'Corolla', 2020, 'available');

UPDATE lyfter_car_rental."user" 
SET status = 'inactive' 
WHERE username = 'prueba';

UPDATE lyfter_car_rental.car 
SET status = 'reserved' 
WHERE make = 'Toyota' and model = 'Corolla' and year = 2020 and status = 'available';

INSERT INTO lyfter_car_rental.car_rental (car_id, user_id, return_date_at, status)
VALUES (12, 12, CURRENT_TIMESTAMP, 'active');

UPDATE lyfter_car_rental.car 
SET status = 'available' 
WHERE make = 'Toyota' and model = 'Corolla' and year = 2020 and status = 'available';

INSERT INTO lyfter_car_rental.car_rental (car_id, user_id, return_date_at, status)
VALUES (12, 12, CURRENT_TIMESTAMP, 'completed');

UPDATE lyfter_car_rental.car 
SET status = 'maintenance' 
WHERE make = 'Toyota' and model = 'Corolla' and year = 2020 and status = 'available';


SELECT * FROM lyfter_car_rental.car 
WHERE status = 'available'

SELECT * FROM lyfter_car_rental.car 
WHERE status = 'rented'