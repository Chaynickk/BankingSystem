

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


COMMENT ON SCHEMA public IS 'standard public schema';


CREATE FUNCTION public.audit_row_change() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
  who text := current_setting('app.user_id', true); -- то, что ты прокинешь из API
  pk_col text;
  pk_val text;
BEGIN
  SELECT a.attname INTO pk_col
  FROM pg_index i
  JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
  WHERE i.indrelid = TG_RELID AND i.indisprimary
  LIMIT 1;

  IF TG_OP = 'INSERT' THEN
    IF pk_col IS NOT NULL THEN
      EXECUTE format('SELECT ($1).%I::text', pk_col) INTO pk_val USING NEW;
    END IF;
    INSERT INTO audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'INSERT', pk_val, NULL, to_jsonb(NEW), who);
    RETURN NEW;

  ELSIF TG_OP = 'UPDATE' THEN
    IF pk_col IS NOT NULL THEN
      EXECUTE format('SELECT ($1).%I::text', pk_col) INTO pk_val USING NEW;
    END IF;
    INSERT INTO audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'UPDATE', pk_val, to_jsonb(OLD), to_jsonb(NEW), who);
    RETURN NEW;

  ELSIF TG_OP = 'DELETE' THEN
    IF pk_col IS NOT NULL THEN
      EXECUTE format('SELECT ($1).%I::text', pk_col) INTO pk_val USING OLD;
    END IF;
    INSERT INTO audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'DELETE', pk_val, to_jsonb(OLD), NULL, who);
    RETURN OLD;
  END IF;

  RETURN NULL;
END;
$_$;


ALTER FUNCTION public.audit_row_change() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.accounts (
    account_id integer NOT NULL,
    client_id integer,
    amount_decimal integer DEFAULT 0 NOT NULL,
    is_frozen boolean DEFAULT false NOT NULL,
    CONSTRAINT amount_decimal CHECK (((amount_decimal <= 1000000000) AND (amount_decimal >= 0)))
);


ALTER TABLE public.accounts OWNER TO postgres;


CREATE SEQUENCE public.accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_account_id_seq OWNER TO postgres;


ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts.account_id;


CREATE TABLE public.admins (
    admin_id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(75) NOT NULL,
    patronymic character varying(75),
    password_hash text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    email character varying(320) NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;


CREATE SEQUENCE public.admins_admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_admin_id_seq OWNER TO postgres;

ALTER SEQUENCE public.admins_admin_id_seq OWNED BY public.admins.admin_id;



CREATE TABLE public.audit_log (
    log_id bigint NOT NULL,
    table_name text NOT NULL,
    op text NOT NULL,
    row_pk text,
    old_data jsonb,
    new_data jsonb,
    changed_by text,
    txid bigint DEFAULT txid_current() NOT NULL,
    changed_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.audit_log OWNER TO postgres;


CREATE SEQUENCE public.audit_log_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_log_log_id_seq OWNER TO postgres;


ALTER SEQUENCE public.audit_log_log_id_seq OWNED BY public.audit_log.log_id;



CREATE TABLE public.clients (
    client_id integer NOT NULL,
    first_name character varying(75) NOT NULL,
    last_name character varying(75) NOT NULL,
    patronymic character varying(75),
    email character varying(320) NOT NULL,
    phone_number character varying(30) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.clients OWNER TO postgres;



CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_client_id_seq OWNER TO postgres;



ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;




CREATE TABLE public.clients_passwords (
    client_id integer NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.clients_passwords OWNER TO postgres;



ALTER TABLE ONLY public.accounts ALTER COLUMN account_id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);




ALTER TABLE ONLY public.admins ALTER COLUMN admin_id SET DEFAULT nextval('public.admins_admin_id_seq'::regclass);



ALTER TABLE ONLY public.audit_log ALTER COLUMN log_id SET DEFAULT nextval('public.audit_log_log_id_seq'::regclass);



ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);




ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- TOC entry 4681 (class 2606 OID 24661)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (admin_id);


--
-- TOC entry 4678 (class 2606 OID 24647)
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4673 (class 2606 OID 24605)
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- TOC entry 4676 (class 1259 OID 24649)
-- Name: audit_log_op_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_log_op_idx ON public.audit_log USING btree (op);


--
-- TOC entry 4679 (class 1259 OID 24648)
-- Name: audit_log_table_name_changed_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_log_table_name_changed_at_idx ON public.audit_log USING btree (table_name, changed_at);


--
-- TOC entry 4686 (class 2620 OID 24664)
-- Name: admins audit_row_change_admin; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER audit_row_change_admin AFTER INSERT OR DELETE OR UPDATE ON public.admins FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4687 (class 2620 OID 24732)
-- Name: clients_passwords audit_row_change_password; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER audit_row_change_password AFTER INSERT OR DELETE OR UPDATE ON public.clients_passwords FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4685 (class 2620 OID 24651)
-- Name: accounts trg_audit_accounts; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_audit_accounts AFTER INSERT OR DELETE OR UPDATE ON public.accounts FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4684 (class 2620 OID 24652)
-- Name: clients trg_audit_clients; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_audit_clients AFTER INSERT OR DELETE OR UPDATE ON public.clients FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4682 (class 2606 OID 24616)
-- Name: accounts accounts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);




ALTER TABLE ONLY public.clients_passwords
    ADD CONSTRAINT clients_passwords_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);

