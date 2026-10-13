--
-- PostgreSQL database dump
--

\restrict sq7W0H1I7Xbc6QpSNqHpJB7y0SL2iwIGctke9YvecC3gL3XPe1YMryOOmnr8kix

-- Dumped from database version 14.24
-- Dumped by pg_dump version 18.6

-- Started on 2026-09-26 13:56:50

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16395)
-- Name: Ejercicio1; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "Ejercicio1";


ALTER SCHEMA "Ejercicio1" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 16410)
-- Name: Bill; Type: TABLE; Schema: Ejercicio1; Owner: postgres
--

CREATE TABLE "Ejercicio1"."Bill" (
    id integer NOT NULL,
    number integer NOT NULL,
    date timestamp without time zone NOT NULL,
    "userId" integer NOT NULL,
    "totalAmount" numeric(18,2) NOT NULL,
    status character varying(15)
);


ALTER TABLE "Ejercicio1"."Bill" OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16422)
-- Name: BillDetail; Type: TABLE; Schema: Ejercicio1; Owner: postgres
--

CREATE TABLE "Ejercicio1"."BillDetail" (
    id integer NOT NULL,
    "productId" integer NOT NULL,
    quantity integer NOT NULL,
    price numeric(18,2) NOT NULL,
    subtotal numeric(18,2) NOT NULL,
    total numeric(18,2) NOT NULL,
    "billId" integer NOT NULL
);


ALTER TABLE "Ejercicio1"."BillDetail" OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16421)
-- Name: BillDetail_id_seq; Type: SEQUENCE; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE "Ejercicio1"."BillDetail" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Ejercicio1"."BillDetail_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 16439)
-- Name: Bill_id_seq; Type: SEQUENCE; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE "Ejercicio1"."Bill" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Ejercicio1"."Bill_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 211 (class 1259 OID 16397)
-- Name: Products; Type: TABLE; Schema: Ejercicio1; Owner: postgres
--

CREATE TABLE "Ejercicio1"."Products" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    stock integer NOT NULL,
    price numeric(18,2) NOT NULL
);


ALTER TABLE "Ejercicio1"."Products" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16396)
-- Name: Products_id_seq; Type: SEQUENCE; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE "Ejercicio1"."Products" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Ejercicio1"."Products_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 213 (class 1259 OID 16403)
-- Name: Users; Type: TABLE; Schema: Ejercicio1; Owner: postgres
--

CREATE TABLE "Ejercicio1"."Users" (
    id integer NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(15) NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE "Ejercicio1"."Users" OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16402)
-- Name: Users_id_seq; Type: SEQUENCE; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE "Ejercicio1"."Users" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "Ejercicio1"."Users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3426 (class 0 OID 16410)
-- Dependencies: 214
-- Data for Name: Bill; Type: TABLE DATA; Schema: Ejercicio1; Owner: postgres
--

COPY "Ejercicio1"."Bill" (id, number, date, "userId", "totalAmount", status) FROM stdin;
1	1001	2026-09-25 10:30:00	3	500.00	Creada
2	1002	2026-09-25 11:00:00	4	150.00	Creada
7	1000	2026-09-26 18:51:37.810219	3	500.00	Creada
8	1003	2026-09-26 19:45:59.984495	3	500.00	Creada
\.


--
-- TOC entry 3428 (class 0 OID 16422)
-- Dependencies: 216
-- Data for Name: BillDetail; Type: TABLE DATA; Schema: Ejercicio1; Owner: postgres
--

COPY "Ejercicio1"."BillDetail" (id, "productId", quantity, price, subtotal, total, "billId") FROM stdin;
1	1	1	500.00	500.00	500.00	1
2	2	2	25.00	50.00	150.00	2
3	3	1	100.00	100.00	150.00	2
5	1	1	1200.00	1200.00	1200.00	7
6	2	1	50.00	50.00	50.00	7
7	1	1	1200.00	1200.00	1200.00	8
8	2	1	50.00	50.00	50.00	8
\.


--
-- TOC entry 3423 (class 0 OID 16397)
-- Dependencies: 211
-- Data for Name: Products; Type: TABLE DATA; Schema: Ejercicio1; Owner: postgres
--

COPY "Ejercicio1"."Products" (id, name, stock, price) FROM stdin;
3	Keyboard Z	30	75.00
1	Laptop X	8	1200.00
2	Mouse Y	48	50.00
\.


--
-- TOC entry 3425 (class 0 OID 16403)
-- Dependencies: 213
-- Data for Name: Users; Type: TABLE DATA; Schema: Ejercicio1; Owner: postgres
--

COPY "Ejercicio1"."Users" (id, username, password, name) FROM stdin;
3	jdoe	12345	John Doe
4	maria	abcde	María Pérez
\.


--
-- TOC entry 3435 (class 0 OID 0)
-- Dependencies: 215
-- Name: BillDetail_id_seq; Type: SEQUENCE SET; Schema: Ejercicio1; Owner: postgres
--

SELECT pg_catalog.setval('"Ejercicio1"."BillDetail_id_seq"', 8, true);


--
-- TOC entry 3436 (class 0 OID 0)
-- Dependencies: 217
-- Name: Bill_id_seq; Type: SEQUENCE SET; Schema: Ejercicio1; Owner: postgres
--

SELECT pg_catalog.setval('"Ejercicio1"."Bill_id_seq"', 8, true);


--
-- TOC entry 3437 (class 0 OID 0)
-- Dependencies: 210
-- Name: Products_id_seq; Type: SEQUENCE SET; Schema: Ejercicio1; Owner: postgres
--

SELECT pg_catalog.setval('"Ejercicio1"."Products_id_seq"', 3, true);


--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 212
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: Ejercicio1; Owner: postgres
--

SELECT pg_catalog.setval('"Ejercicio1"."Users_id_seq"', 4, true);


--
-- TOC entry 3277 (class 2606 OID 16426)
-- Name: BillDetail BillDetail_pkey; Type: CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."BillDetail"
    ADD CONSTRAINT "BillDetail_pkey" PRIMARY KEY (id);


--
-- TOC entry 3274 (class 2606 OID 16414)
-- Name: Bill Bill_pkey; Type: CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."Bill"
    ADD CONSTRAINT "Bill_pkey" PRIMARY KEY (id);


--
-- TOC entry 3268 (class 2606 OID 16401)
-- Name: Products Products_pkey; Type: CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."Products"
    ADD CONSTRAINT "Products_pkey" PRIMARY KEY (id);


--
-- TOC entry 3270 (class 2606 OID 16407)
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- TOC entry 3272 (class 2606 OID 16409)
-- Name: Users uq_username; Type: CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."Users"
    ADD CONSTRAINT uq_username UNIQUE (username);


--
-- TOC entry 3278 (class 1259 OID 16438)
-- Name: fki_B; Type: INDEX; Schema: Ejercicio1; Owner: postgres
--

CREATE INDEX "fki_B" ON "Ejercicio1"."BillDetail" USING btree ("productId");


--
-- TOC entry 3279 (class 1259 OID 16432)
-- Name: fki_FK_BillDetail_Bill; Type: INDEX; Schema: Ejercicio1; Owner: postgres
--

CREATE INDEX "fki_FK_BillDetail_Bill" ON "Ejercicio1"."BillDetail" USING btree ("billId");


--
-- TOC entry 3275 (class 1259 OID 16420)
-- Name: fki_FK_Bill_Users; Type: INDEX; Schema: Ejercicio1; Owner: postgres
--

CREATE INDEX "fki_FK_Bill_Users" ON "Ejercicio1"."Bill" USING btree ("userId");


--
-- TOC entry 3281 (class 2606 OID 16427)
-- Name: BillDetail FK_BillDetail_Bill; Type: FK CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."BillDetail"
    ADD CONSTRAINT "FK_BillDetail_Bill" FOREIGN KEY ("billId") REFERENCES "Ejercicio1"."Bill"(id) NOT VALID;


--
-- TOC entry 3282 (class 2606 OID 16433)
-- Name: BillDetail FK_BillDetail_Product; Type: FK CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."BillDetail"
    ADD CONSTRAINT "FK_BillDetail_Product" FOREIGN KEY ("productId") REFERENCES "Ejercicio1"."Products"(id) NOT VALID;


--
-- TOC entry 3280 (class 2606 OID 16415)
-- Name: Bill FK_Bill_Users; Type: FK CONSTRAINT; Schema: Ejercicio1; Owner: postgres
--

ALTER TABLE ONLY "Ejercicio1"."Bill"
    ADD CONSTRAINT "FK_Bill_Users" FOREIGN KEY ("userId") REFERENCES "Ejercicio1"."Users"(id) ON UPDATE RESTRICT ON DELETE RESTRICT NOT VALID;


-- Completed on 2026-09-26 13:56:50

--
-- PostgreSQL database dump complete
--

\unrestrict sq7W0H1I7Xbc6QpSNqHpJB7y0SL2iwIGctke9YvecC3gL3XPe1YMryOOmnr8kix

