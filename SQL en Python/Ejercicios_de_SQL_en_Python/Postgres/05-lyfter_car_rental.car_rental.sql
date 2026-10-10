-- Table: lyfter_car_rental.car_rental

-- DROP TABLE IF EXISTS lyfter_car_rental.car_rental;

CREATE TABLE IF NOT EXISTS lyfter_car_rental.car_rental
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    car_id integer NOT NULL,
    user_id integer NOT NULL,
    rental_date_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    return_date_at timestamp,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_car_rental PRIMARY KEY (id),
    CONSTRAINT fk_car_rental_car FOREIGN KEY (car_id)
        REFERENCES lyfter_car_rental.car (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_car_rental_user FOREIGN KEY (user_id)
        REFERENCES lyfter_car_rental."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS lyfter_car_rental.car_rental
    OWNER to postgres;

INSERT INTO lyfter_car_rental.car_rental (car_id, user_id, return_date_at, status) 
VALUES
(1, 1, '2026-10-10', 'active'),
(2, 5, '2026-10-12', 'completed'),
(3, 10, '2026-10-15', 'cancelled'),
(4, 20, '2026-10-18', 'overdue'),
(5, 25, '2026-10-20', 'pending');
