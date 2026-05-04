# SQL and Databases

**Design schemas, write queries, and avoid common pitfalls across SQLite, PostgreSQL, and MySQL.**

SQL is one of the skills LLMs get wrong most often — generating queries that work in simple tests but fail under real data: N+1 problems, missing indexes, broken transactions, injection vulnerabilities. This skill covers the patterns that matter.

---

## Schema Design

### Normalization Basics

**First Normal Form (1NF):** No repeating groups. Each column has a single value.
```sql
-- WRONG: comma-separated values in one column
CREATE TABLE posts (id INT, tags TEXT); -- tags = "ai,python,llm"

-- RIGHT: separate table for the relationship
CREATE TABLE post_tags (post_id INT, tag TEXT, PRIMARY KEY (post_id, tag));
```

**Third Normal Form (3NF):** No transitive dependencies — non-key columns depend only on the primary key, not on other non-key columns.
```sql
-- WRONG: city_population depends on city, not user_id
CREATE TABLE users (user_id INT PRIMARY KEY, city TEXT, city_population INT);

-- RIGHT: separate the city data
CREATE TABLE cities (city TEXT PRIMARY KEY, population INT);
CREATE TABLE users (user_id INT PRIMARY KEY, city TEXT REFERENCES cities(city));
```

### Primary Keys

```sql
-- Use SERIAL / IDENTITY for surrogate keys (simpler)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,         -- PostgreSQL
    -- id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Use UUIDs for distributed systems or public-facing IDs
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT REFERENCES users(id)
);
```

### Foreign Keys and Cascades

```sql
-- Always declare foreign keys explicitly
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

`ON DELETE CASCADE`: deletes posts when user is deleted  
`ON DELETE SET NULL`: sets FK to NULL (must be nullable)  
`ON DELETE RESTRICT` (default): prevents deleting a user who has posts

---

## Indexing

Without indexes, every query is a full table scan. Add them for columns you filter or join on.

```sql
-- Index on a frequently filtered column
CREATE INDEX idx_posts_author ON posts(author_id);

-- Composite index for queries that filter on two columns together
CREATE INDEX idx_posts_author_created ON posts(author_id, created_at DESC);

-- Unique index (also enforces constraint)
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Partial index (only index rows matching a condition — smaller, faster)
CREATE INDEX idx_posts_published ON posts(created_at) WHERE published = TRUE;
```

**When to add an index:**
- Columns in `WHERE` clauses
- Columns in `JOIN` conditions (foreign keys)
- Columns in `ORDER BY` when used with `LIMIT`
- Columns with high cardinality (many unique values)

**When NOT to add an index:**
- Columns rarely used in queries
- Boolean columns (low cardinality — index rarely helps)
- Very small tables (< 1000 rows — full scan is faster)

---

## Common Query Patterns

### Pagination
```sql
-- Offset pagination (simple but slow on large offsets)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 40;

-- Cursor pagination (fast regardless of depth)
SELECT * FROM posts
WHERE created_at < '2024-01-15T10:00:00Z'  -- cursor from last page
ORDER BY created_at DESC
LIMIT 20;
```

### Aggregation
```sql
-- Count with group
SELECT author_id, COUNT(*) AS post_count
FROM posts
GROUP BY author_id
ORDER BY post_count DESC;

-- Filter aggregated groups with HAVING
SELECT author_id, COUNT(*) AS post_count
FROM posts
GROUP BY author_id
HAVING COUNT(*) > 10;
```

### JOINs
```sql
-- INNER JOIN: only rows that match in both tables
SELECT u.email, p.title
FROM posts p
INNER JOIN users u ON p.author_id = u.id;

-- LEFT JOIN: all posts, even those without an author (shouldn't happen but defensive)
SELECT p.title, u.email
FROM posts p
LEFT JOIN users u ON p.author_id = u.id;

-- Avoid N+1: don't query in a loop
-- BAD: 1 query per post
for post in posts:
    author = db.query(f"SELECT * FROM users WHERE id = {post.author_id}")

-- GOOD: 1 query total
SELECT p.*, u.email AS author_email
FROM posts p
JOIN users u ON p.author_id = u.id;
```

### Upsert (Insert or Update)
```sql
-- PostgreSQL
INSERT INTO user_settings (user_id, theme, notifications)
VALUES (42, 'dark', true)
ON CONFLICT (user_id) DO UPDATE SET
    theme = EXCLUDED.theme,
    notifications = EXCLUDED.notifications;

-- SQLite
INSERT OR REPLACE INTO user_settings (user_id, theme, notifications)
VALUES (42, 'dark', true);
```

---

## Transactions

Wrap multiple related writes in a transaction. Either all succeed or none do.

```python
# Python with sqlite3
import sqlite3
conn = sqlite3.connect("db.sqlite")
try:
    conn.execute("BEGIN")
    conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = ?", (sender_id,))
    conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = ?", (receiver_id,))
    conn.commit()
except Exception:
    conn.rollback()
    raise

# Python with psycopg2
with psycopg2.connect(DSN) as conn:
    with conn.cursor() as cur:
        cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = %s", (sender_id,))
        cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = %s", (receiver_id,))
    # conn.commit() happens automatically on context exit
```

---

## Parameterized Queries (Security)

Never use string formatting for SQL. Always use parameterized queries.

```python
# NEVER (SQL injection risk)
query = f"SELECT * FROM users WHERE username = '{username}'"

# SQLite — use ?
cur.execute("SELECT * FROM users WHERE username = ?", (username,))

# PostgreSQL (psycopg2) — use %s
cur.execute("SELECT * FROM users WHERE username = %s", (username,))

# SQLAlchemy — use text() with named params
from sqlalchemy import text
result = db.execute(text("SELECT * FROM users WHERE username = :name"), {"name": username})
```

---

## SQLite vs PostgreSQL vs MySQL

| Feature | SQLite | PostgreSQL | MySQL |
|---|---|---|---|
| Setup | Zero — file-based | Server process | Server process |
| Concurrent writes | Limited (file lock) | Full | Full |
| JSON support | Basic | Excellent (JSONB) | Good |
| Full text search | FTS5 extension | tsvector/tsquery | FULLTEXT |
| Window functions | Yes (3.25+) | Yes | Yes (8.0+) |
| Best for | Embedded, dev, testing | Production web apps | Legacy systems, hosting |

**Rule:** Use SQLite for local tools, scripts, and development. Use PostgreSQL for anything production.

---

## ORM vs Raw SQL

**Use an ORM (SQLAlchemy, Django ORM, Tortoise):**
- For CRUD operations and simple queries
- When you want schema migrations managed for you
- When query portability between databases matters

**Use raw SQL:**
- For complex analytics queries with multiple CTEs/window functions
- When performance is critical and you need to control the query plan
- When the ORM-generated SQL is slow and hard to optimize

**You can mix both.** Use the ORM for standard operations, raw SQL for the 10% of queries that need it.

---

## Query Performance Debugging (PostgreSQL)

```sql
-- EXPLAIN shows the query plan
EXPLAIN SELECT * FROM posts WHERE author_id = 42;

-- EXPLAIN ANALYZE actually runs the query and shows timings
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 42;

-- Look for:
-- Seq Scan on large tables → missing index
-- Nested Loop with large row counts → N+1 or missing join index
-- High actual time vs estimated → stale statistics → run ANALYZE
```

---

## Pairs Well With

- `secure-coding` — parameterized queries and injection prevention
- `spec-first-development` — design your schema before writing code
- `structured-output-local` — return query results as typed JSON

---

## License

CC0-1.0 — public domain, free to use for any purpose.
