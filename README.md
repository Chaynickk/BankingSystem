### ⚙️ Настройка `.env`

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>
SECRET_KEY=<секретный_ключ>
ALGORITHM=<алгоритм_хэширования>
MAX_BALANCE=<макс_баланс_в_сотнях>
```

**Пример:**

```env
DATABASE_URL=postgresql+asyncpg://postgres:1234@localhost:5432/banking
SECRET_KEY=mysecretkey123
ALGORITHM=HS256
MAX_BALANCE=100000
```

**Что это значит:**

* `DATABASE_URL` — строка подключения к PostgreSQL
* `SECRET_KEY` — ключ для токенов и хэширования
* `ALGORITHM` — тип алгоритма (например `HS256`)
* `MAX_BALANCE` — максимальный баланс на счёте, **указывается в “сотнях”**

  > То есть если поставить `100`, клиент увидит `1.00`.

## 1) Установка зависимостей

```bash
# клонируем
git clone <url_вашего_репо>
cd BankingSystem

# (опционально) создаём venv
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# ставим пакеты
pip install -r requirements.txt
```

> Рекомед: Python 3.10+ и свежий `pip`.

---

## 2) Развёртывание базы данных

У вас должен быть PostgreSQL (локально или в контейнере). Создание схемы делаем из SQL-скрипта.

Путь к скрипту:

```
BankingSystem\db\Create_db
```

---

## 3) Проверка триггеров аудита

Нам нужны триггеры (и функция `audit_row_change()`) на таблицах:

* `accounts`
* `admins`
* `clients`
* `clients_password`

В UI это должно выглядеть как на скрине:
`Triggers -> trg_audit_<table> -> audit_row_change()`.

### Если триггеры **не появились** — выполняем этот код

> Запускайте **под пользователем, у которого есть право создавать триггеры** на этих таблицах.

```sql
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
```

---

## 4) Активируем первого админа вручную

По дефолту первый админ не активирован. Нужно руками выставить `is_active = true`.

```sql
UPDATE admins
SET is_active = TRUE
WHERE email = '<email_вашего_админа>';
```
