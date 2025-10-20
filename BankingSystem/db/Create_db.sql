--
-- PostgreSQL database dump
--

\restrict bz6PpirSF2Omab9F4zLtlg7vmihB42k8DNE5dZ5fTWRAppBDGgBtKKcgRzeOPwV

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

-- Started on 2025-10-17 13:00:55

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4839 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 237 (class 1255 OID 24650)
-- Name: audit_row_change(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.audit_row_change() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
  who text := current_setting('app.user_id', true); -- то, что ты прокинешь из API
  pk_col text;
  pk_val text;
BEGIN
  -- находим имя PK-колонки (опционально)
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

--
-- TOC entry 220 (class 1259 OID 24607)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    account_id integer NOT NULL,
    client_id integer,
    amount_decimal integer DEFAULT 0 NOT NULL,
    is_frozen boolean DEFAULT false NOT NULL,
    CONSTRAINT amount_decimal CHECK (((amount_decimal <= 1000000000) AND (amount_decimal >= 0)))
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24606)
-- Name: accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_account_id_seq OWNER TO postgres;

--
-- TOC entry 4840 (class 0 OID 0)
-- Dependencies: 219
-- Name: accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts.account_id;


--
-- TOC entry 224 (class 1259 OID 24654)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    admin_id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(75) NOT NULL,
    patronymic character varying(75),
    password_hash text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    email character varying(320) NOT NULL,
    is_active boolean DEFAULT false NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24653)
-- Name: admins_admin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_admin_id_seq OWNER TO postgres;

--
-- TOC entry 4841 (class 0 OID 0)
-- Dependencies: 223
-- Name: admins_admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_admin_id_seq OWNED BY public.admins.admin_id;


--
-- TOC entry 222 (class 1259 OID 24638)
-- Name: audit_log; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- TOC entry 221 (class 1259 OID 24637)
-- Name: audit_log_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_log_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_log_log_id_seq OWNER TO postgres;

--
-- TOC entry 4842 (class 0 OID 0)
-- Dependencies: 221
-- Name: audit_log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_log_log_id_seq OWNED BY public.audit_log.log_id;


--
-- TOC entry 218 (class 1259 OID 24598)
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- TOC entry 217 (class 1259 OID 24597)
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_client_id_seq OWNER TO postgres;

--
-- TOC entry 4843 (class 0 OID 0)
-- Dependencies: 217
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- TOC entry 225 (class 1259 OID 24722)
-- Name: clients_passwords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients_passwords (
    client_id integer NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.clients_passwords OWNER TO postgres;

--
-- TOC entry 4663 (class 2604 OID 24665)
-- Name: accounts account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN account_id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);


--
-- TOC entry 4669 (class 2604 OID 24666)
-- Name: admins admin_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN admin_id SET DEFAULT nextval('public.admins_admin_id_seq'::regclass);


--
-- TOC entry 4666 (class 2604 OID 24667)
-- Name: audit_log log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_log ALTER COLUMN log_id SET DEFAULT nextval('public.audit_log_log_id_seq'::regclass);


--
-- TOC entry 4661 (class 2604 OID 24668)
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- TOC entry 4676 (class 2606 OID 24615)
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- TOC entry 4682 (class 2606 OID 24661)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (admin_id);


--
-- TOC entry 4679 (class 2606 OID 24647)
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4674 (class 2606 OID 24605)
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- TOC entry 4677 (class 1259 OID 24649)
-- Name: audit_log_op_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_log_op_idx ON public.audit_log USING btree (op);


--
-- TOC entry 4680 (class 1259 OID 24648)
-- Name: audit_log_table_name_changed_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_log_table_name_changed_at_idx ON public.audit_log USING btree (table_name, changed_at);


--
-- TOC entry 4687 (class 2620 OID 24664)
-- Name: admins audit_row_change_admin; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER audit_row_change_admin AFTER INSERT OR DELETE OR UPDATE ON public.admins FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4688 (class 2620 OID 24732)
-- Name: clients_passwords audit_row_change_password; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER audit_row_change_password AFTER INSERT OR DELETE OR UPDATE ON public.clients_passwords FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4686 (class 2620 OID 24651)
-- Name: accounts trg_audit_accounts; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_audit_accounts AFTER INSERT OR DELETE OR UPDATE ON public.accounts FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4685 (class 2620 OID 24652)
-- Name: clients trg_audit_clients; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_audit_clients AFTER INSERT OR DELETE OR UPDATE ON public.clients FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();


--
-- TOC entry 4683 (class 2606 OID 24616)
-- Name: accounts accounts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


--
-- TOC entry 4684 (class 2606 OID 24727)
-- Name: clients_passwords clients_passwords_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients_passwords
    ADD CONSTRAINT clients_passwords_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


-- Completed on 2025-10-17 13:00:55

--
-- PostgreSQL database dump complete
--

\unrestrict bz6PpirSF2Omab9F4zLtlg7vmihB42k8DNE5dZ5fTWRAppBDGgBtKKcgRzeOPwV


-- чтобы видеть реальную ошибку, если будет
\set ON_ERROR_STOP on

-- (опционально) убедимся, что язык есть
CREATE EXTENSION IF NOT EXISTS plpgsql;


-- функция (оставлю как у тебя)
CREATE OR REPLACE FUNCTION public.audit_row_change()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  who    text := current_setting('app.user_id', true);
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
    INSERT INTO public.audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'INSERT', pk_val, NULL, to_jsonb(NEW), who);
    RETURN NEW;

  ELSIF TG_OP = 'UPDATE' THEN
    IF pk_col IS NOT NULL THEN
      EXECUTE format('SELECT ($1).%I::text', pk_col) INTO pk_val USING NEW;
    END IF;
    INSERT INTO public.audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'UPDATE', pk_val, to_jsonb(OLD), to_jsonb(NEW), who);
    RETURN NEW;

  ELSIF TG_OP = 'DELETE' THEN
    IF pk_col IS NOT NULL THEN
      EXECUTE format('SELECT ($1).%I::text', pk_col) INTO pk_val USING OLD;
    END IF;
    INSERT INTO public.audit_log(table_name, op, row_pk, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, 'DELETE', pk_val, to_jsonb(OLD), NULL, who);
    RETURN OLD;
  END IF;

  RETURN NULL;
END;
$$;

-- чтобы не проглатывать фейлы на отладке
\set ON_ERROR_STOP on

-- (опционально) отдать владение одному юзеру
-- ALTER TABLE    ALL IN SCHEMA public OWNER TO myuser;
-- ALTER SEQUENCE ALL IN SCHEMA public OWNER TO myuser;
-- ALTER FUNCTION public.audit_row_change() OWNER TO myuser;

-- повесить триггеры на всё, кроме audit_log, если их ещё нет
DO $$
DECLARE
  r RECORD; trg_name text;
BEGIN
  FOR r IN
    SELECT n.nspname sch, c.relname tbl
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind='r' AND n.nspname='public' AND c.relname <> 'audit_log'
  LOOP
    trg_name := 'trg_audit_'||r.tbl;

    IF NOT EXISTS (
      SELECT 1 FROM pg_trigger t
      JOIN pg_class c2 ON c2.oid=t.tgrelid
      JOIN pg_namespace n2 ON n2.oid=c2.relnamespace
      WHERE NOT t.tgisinternal
        AND t.tgname=trg_name AND n2.nspname=r.sch AND c2.relname=r.tbl
    ) THEN
      -- проверка привилегии, чтобы не падать, если запускают «не тем» юзером
      IF has_table_privilege(current_user, format('%I.%I', r.sch, r.tbl), 'TRIGGER') THEN
        EXECUTE format(
          'CREATE TRIGGER %I
             AFTER INSERT OR UPDATE OR DELETE ON %I.%I
           FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();',
          trg_name, r.sch, r.tbl
        );
      END IF;
    END IF;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
