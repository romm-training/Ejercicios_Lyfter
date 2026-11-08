-- Table: lyfter_car_rental.car

-- DROP TABLE IF EXISTS lyfter_car_rental.car;

CREATE TABLE IF NOT EXISTS lyfter_car_rental.car
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    make character varying(50) COLLATE pg_catalog."default" NOT NULL,
    model character varying(50) COLLATE pg_catalog."default" NOT NULL,
    year integer NOT NULL,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_car PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS lyfter_car_rental.car
    OWNER to postgres;

INSERT INTO lyfter_car_rental.car (make, model, year, status) 
VALUES
('Toyota', 'Corolla', 2018, 'available'),
('Honda', 'Civic', 2019, 'rented'),
('Ford', 'Focus', 2015, 'maintenance'),
('Chevrolet', 'Cruze', 2020, 'reserved'),
('Nissan', 'Sentra', 2017, 'sold'),
('Hyundai', 'Elantra', 2016, 'inactive'),
('Kia', 'Rio', 2021, 'available'),
('Volkswagen', 'Jetta', 2014, 'rented'),
('Mazda', '3', 2013, 'maintenance'),
('Subaru', 'Impreza', 2022, 'available'),
('BMW', '320i', 2019, 'reserved'),
('Mercedes-Benz', 'C200', 2021, 'available'),
('Audi', 'A4', 2018, 'rented'),
('Peugeot', '308', 2015, 'maintenance'),
('Renault', 'Clio', 2016, 'available'),
('Fiat', '500', 2012, 'sold'),
('Skoda', 'Octavia', 2020, 'available'),
('Seat', 'Leon', 2017, 'inactive'),
('Volvo', 'S60', 2019, 'rented'),
('Jaguar', 'XE', 2021, 'reserved'),
('Toyota', 'Yaris', 2013, 'available'),
('Honda', 'Accord', 2015, 'rented'),
('Ford', 'Fusion', 2018, 'available'),
('Chevrolet', 'Malibu', 2017, 'maintenance'),
('Nissan', 'Altima', 2019, 'sold'),
('Hyundai', 'Sonata', 2020, 'available'),
('Kia', 'Optima', 2016, 'inactive'),
('Volkswagen', 'Passat', 2014, 'available'),
('Mazda', '6', 2018, 'rented'),
('Subaru', 'Legacy', 2017, 'available'),
('BMW', 'X1', 2020, 'reserved'),
('Mercedes-Benz', 'GLA', 2021, 'available'),
('Audi', 'Q3', 2019, 'rented'),
('Peugeot', '2008', 2018, 'available'),
('Renault', 'Captur', 2020, 'maintenance'),
('Fiat', 'Punto', 2015, 'inactive'),
('Skoda', 'Superb', 2019, 'available'),
('Seat', 'Ibiza', 2016, 'rented'),
('Volvo', 'XC40', 2022, 'available'),
('Jaguar', 'F-Pace', 2021, 'reserved'),
('Toyota', 'Camry', 2018, 'available'),
('Honda', 'HR-V', 2019, 'rented'),
('Ford', 'Escape', 2020, 'available'),
('Chevrolet', 'Equinox', 2021, 'maintenance'),
('Nissan', 'Rogue', 2017, 'sold'),
('Hyundai', 'Tucson', 2018, 'available'),
('Kia', 'Sportage', 2019, 'inactive'),
('Volkswagen', 'Tiguan', 2020, 'available'),
('Mazda', 'CX-5', 2021, 'rented'),
('Subaru', 'Forester', 2022, 'available');
