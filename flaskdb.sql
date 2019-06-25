--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.articles (
    title character varying(100) NOT NULL,
    body character varying(1000) NOT NULL,
    author character varying(100) NOT NULL,
    id integer NOT NULL,
    create_date character varying(100) NOT NULL
);


ALTER TABLE public.articles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.articles (title, body, author, id, create_date) FROM stdin;
THIS IS ARTICLE ONE	<p><strong>KEVIN KEMBOI</strong></p>	KEVIN KEMBOI	1	06-06-2019
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (name, email, username, password) FROM stdin;
Kevin kemboi	kkemboi08@gmail.com	kevin	$5$rounds=535000$.O0WZs45l4j/Llnh$DEQSH9yWQr9wr1QWD5jfffvbmYKToFHAbzlAvuO2bH4
\.


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- PostgreSQL database dump complete
--

