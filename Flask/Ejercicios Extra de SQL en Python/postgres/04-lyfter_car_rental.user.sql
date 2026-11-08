-- Table: lyfter_car_rental.user

-- DROP TABLE IF EXISTS lyfter_car_rental."user";

CREATE TABLE IF NOT EXISTS lyfter_car_rental."user"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(20) COLLATE pg_catalog."default" NOT NULL,
    birthdate_at date NOT NULL,
    account_status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY (id),
    CONSTRAINT uq_user_email UNIQUE (email),
    CONSTRAINT uq_user_username UNIQUE (username)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS lyfter_car_rental."user"
    OWNER to postgres;

INSERT INTO lyfter_car_rental."user" (name, email, username, password, birthdate_at, account_status) 
VALUES
('Alice Johnson', 'alice.johnson1@example.com', 'alicej1', 'pass1234', '1990-05-12', 'active'),
('Bob Smith', 'bob.smith2@example.com', 'bobsmith2', 'secure567', '1985-03-22', 'active'),
('Charlie Brown', 'charlie.brown3@example.com', 'charlieb3', 'mypwd890', '1992-07-14', 'inactive'),
('Diana Prince', 'diana.prince4@example.com', 'dianap4', 'wonder123', '1988-11-30', 'active'),
('Ethan Hunt', 'ethan.hunt5@example.com', 'ethanh5', 'mission999', '1979-01-17', 'active'),
('Fiona Gallagher', 'fiona.gallagher6@example.com', 'fionag6', 'pwd45678', '1995-09-09', 'inactive'),
('George Miller', 'george.miller7@example.com', 'georgem7', 'george777', '1983-04-25', 'active'),
('Hannah Davis', 'hannah.davis8@example.com', 'hannahd8', 'hannah888', '1991-02-13', 'active'),
('Ian Curtis', 'ian.curtis9@example.com', 'ianc9', 'joydiv99', '1976-07-15', 'inactive'),
('Julia Roberts', 'julia.roberts10@example.com', 'juliar10', 'pretty123', '1967-10-28', 'active'),
('Kevin Hart', 'kevin.hart11@example.com', 'kevinh11', 'laughs11', '1979-07-06', 'active'),
('Laura Palmer', 'laura.palmer12@example.com', 'laurap12', 'twinpeaks', '1970-07-22', 'inactive'),
('Michael Scott', 'michael.scott13@example.com', 'michaels13', 'dunderm13', '1964-03-15', 'active'),
('Nancy Drew', 'nancy.drew14@example.com', 'nancyd14', 'detective14', '1993-06-18', 'active'),
('Oscar Wilde', 'oscar.wilde15@example.com', 'oscarw15', 'writer15', '1854-10-16', 'inactive'),
('Paula Abdul', 'paula.abdul16@example.com', 'paulaa16', 'dance16', '1962-06-19', 'active'),
('Quentin Blake', 'quentin.blake17@example.com', 'quentinb17', 'artist17', '1932-12-25', 'active'),
('Rachel Green', 'rachel.green18@example.com', 'rachelg18', 'friends18', '1969-05-05', 'active'),
('Sam Wilson', 'sam.wilson19@example.com', 'samw19', 'falcon19', '1980-09-23', 'inactive'),
('Tina Fey', 'tina.fey20@example.com', 'tinaf20', 'comedy20', '1970-05-18', 'active'),
('Uma Thurman', 'uma.thurman21@example.com', 'umat21', 'killbill21', '1970-04-29', 'active'),
('Victor Hugo', 'victor.hugo22@example.com', 'victorh22', 'lesmis22', '1802-02-26', 'inactive'),
('Wendy Darling', 'wendy.darling23@example.com', 'wendyd23', 'peterpan23', '1900-07-01', 'active'),
('Xavier Woods', 'xavier.woods24@example.com', 'xavierw24', 'wwe24', '1986-09-04', 'active'),
('Yara Shahidi', 'yara.shahidi25@example.com', 'yaras25', 'grownish25', '2000-02-10', 'active'),
('Zoe Kravitz', 'zoe.kravitz26@example.com', 'zoek26', 'batman26', '1988-12-01', 'inactive'),
('Adam Levine', 'adam.levine27@example.com', 'adaml27', 'maroon27', '1979-03-18', 'active'),
('Bella Swan', 'bella.swan28@example.com', 'bellas28', 'twilight28', '1987-09-13', 'active'),
('Chris Evans', 'chris.evans29@example.com', 'chrise29', 'cap29', '1981-06-13', 'active'),
('Donna Noble', 'donna.noble30@example.com', 'donnan30', 'doctor30', '1970-12-25', 'inactive'),
('Edward Norton', 'edward.norton31@example.com', 'edwardn31', 'fightclub31', '1969-08-18', 'active'),
('Frida Kahlo', 'frida.kahlo32@example.com', 'fridak32', 'art32', '1907-07-06', 'inactive'),
('Greg House', 'greg.house33@example.com', 'gregh33', 'house33', '1959-05-15', 'active'),
('Hermione Granger', 'hermione.granger34@example.com', 'hermioneg34', 'hogwarts34', '1979-09-19', 'active'),
('Indiana Jones', 'indiana.jones35@example.com', 'indianaj35', 'adventure35', '1899-07-01', 'inactive'),
('Jack Sparrow', 'jack.sparrow36@example.com', 'jacks36', 'pirate36', '1963-06-09', 'active'),
('Katniss Everdeen', 'katniss.everdeen37@example.com', 'katniss37', 'mocking37', '1990-05-08', 'active'),
('Luke Skywalker', 'luke.skywalker38@example.com', 'lukes38', 'force38', '1951-09-25', 'active'),
('Mona Lisa', 'mona.lisa39@example.com', 'monal39', 'painting39', '1503-06-01', 'inactive'),
('Neo Anderson', 'neo.anderson40@example.com', 'neoa40', 'matrix40', '1964-03-11', 'active'),
('Oprah Winfrey', 'oprah.winfrey41@example.com', 'oprahw41', 'talkshow41', '1954-01-29', 'active'),
('Peter Parker', 'peter.parker42@example.com', 'peterp42', 'spiderman42', '1995-08-10', 'active'),
('Queen Elizabeth', 'queen.elizabeth43@example.com', 'queene43', 'royal43', '1926-04-21', 'inactive'),
('Ron Weasley', 'ron.weasley44@example.com', 'ronw44', 'hogwarts44', '1980-03-01', 'active'),
('Sarah Connor', 'sarah.connor45@example.com', 'sarahc45', 'terminator45', '1965-05-13', 'active'),
('Tony Stark', 'tony.stark46@example.com', 'tonys46', 'ironman46', '1970-05-29', 'active'),
('Ursula K Le Guin', 'ursula.leguin47@example.com', 'ursulal47', 'earthsea47', '1929-10-21', 'inactive'),
('Vin Diesel', 'vin.diesel48@example.com', 'vind48', 'fast48', '1967-07-18', 'active'),
('Walter White', 'walter.white49@example.com', 'walterw49', 'heisen49', '1959-09-07', 'active'),
('Xena Warrior', 'xena.warrior50@example.com', 'xenaw50', 'xena50', '1970-01-01', 'active');
