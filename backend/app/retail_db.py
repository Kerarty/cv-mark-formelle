"""SQLite-демо ритейл-схемы: честные планы запросов на 200k строк.

Индексы создаются при старте. «Медленный» прогон форсируется через ``NOT INDEXED``
(план остаётся SCAN), «быстрый» — штатный: планировщик ищет по индексу. Эффект
индекса виден и в плане, и во времени. Произвольный SQL от клиента не исполняется —
только запросы из реестра ``DEMO_QUERIES``.
"""

import random
import sqlite3
import threading
import time
from dataclasses import dataclass

ROW_COUNT = 200_000
CITIES = [
    "Минск",
    "Заславль",
    "Брест",
    "Гродно",
    "Гомель",
    "Витебск",
    "Могилёв",
    "Бобруйск",
    "Мозырь",
    "Пинск",
    "Барановичи",
    "Полоцк",
]
CATEGORIES = [
    "боди",
    "бюстгальтер",
    "трусы",
    "футболка",
    "свитшот",
    "джинсы",
    "леггинсы",
    "носок",
    "пижама",
    "купальник",
]
STATUSES = ["shipped"] * 4 + ["received"] * 3 + ["reserved"] * 2 + ["cancelled"]

TABLES = [
    ("stores", "50 магазинов сети — 4 страны, у Марк Формэль их 330+"),
    ("products", "500 SKU: бельё и одежда, единственный источник для JOIN"),
    ("stock_movements", "200 000 движений: отгрузки, приёмки, резервы, отмены"),
]


@dataclass(frozen=True)
class DemoQuery:
    id: str
    title: str
    description: str
    tsql: str  # витрина в T-SQL (MS SQL Server) — что HR видит в UI
    sql: str  # исполняемый SQLite-вариант, быстрый прогон
    slow_sql: str  # вариант с NOT INDEXED — честный SCAN для сравнения
    index_name: str
    index_sql: str


DEMO_QUERIES: dict[str, DemoQuery] = {
    "stock-report": DemoQuery(
        id="stock-report",
        title="Отчёт по отгрузкам за 3 дня",
        description=(
            "Классика товародвижения: агрегат по витрине-остаткам за период. "
            "Без индекса — полный скан 200 000 движений; составной индекс "
            "(status, moved_at) превращает его в точечный поиск по диапазону."
        ),
        tsql="""\
SELECT s.name, COUNT(*) AS movements, SUM(m.qty) AS total_qty
FROM stock_movements m
JOIN stores s ON s.store_id = m.store_id
WHERE m.status = 'shipped'
  AND m.moved_at BETWEEN '2026-11-27' AND '2026-11-30'
GROUP BY s.name
ORDER BY total_qty DESC;

-- эффект индекса:
CREATE INDEX idx_movements_status_date ON stock_movements (status, moved_at);""",
        sql="""\
SELECT s.name AS store, COUNT(*) AS movements, SUM(m.qty) AS total_qty
FROM stock_movements AS m
JOIN stores AS s ON s.store_id = m.store_id
WHERE m.status = 'shipped'
  AND m.moved_at BETWEEN '2026-11-27' AND '2026-11-30'
GROUP BY s.name
ORDER BY total_qty DESC""",
        slow_sql="""\
SELECT s.name AS store, COUNT(*) AS movements, SUM(m.qty) AS total_qty
FROM stock_movements AS m NOT INDEXED
JOIN stores AS s ON s.store_id = m.store_id
WHERE m.status = 'shipped'
  AND m.moved_at BETWEEN '2026-11-27' AND '2026-11-30'
GROUP BY s.name
ORDER BY total_qty DESC""",
        index_name="idx_movements_status_date",
        index_sql="CREATE INDEX idx_movements_status_date ON stock_movements (status, moved_at)",
    ),
    "product-detail": DemoQuery(
        id="product-detail",
        title="Детализация по одному SKU",
        description=(
            "Точечная детализация движения товара — запрос, который витрина "
            "дёргает при каждом открытии карточки. Внешний ключ без индекса = "
            "скан всей таблицы движений на каждый клик."
        ),
        tsql="""\
SELECT m.id, s.name, m.qty, m.moved_at
FROM stock_movements m
JOIN stores s ON s.store_id = m.store_id
WHERE m.product_id = (SELECT product_id FROM products WHERE sku = 'MF-00042')
ORDER BY m.moved_at DESC;

-- эффект индекса:
CREATE INDEX idx_movements_product ON stock_movements (product_id);""",
        sql="""\
SELECT m.id, s.name AS store, m.qty, m.moved_at
FROM stock_movements AS m
JOIN stores AS s ON s.store_id = m.store_id
WHERE m.product_id = (SELECT product_id FROM products WHERE sku = 'MF-00042')
ORDER BY m.moved_at DESC
LIMIT 50""",
        slow_sql="""\
SELECT m.id, s.name AS store, m.qty, m.moved_at
FROM stock_movements AS m NOT INDEXED
JOIN stores AS s ON s.store_id = m.store_id
WHERE m.product_id = (SELECT product_id FROM products WHERE sku = 'MF-00042')
ORDER BY m.moved_at DESC
LIMIT 50""",
        index_name="idx_movements_product",
        index_sql="CREATE INDEX idx_movements_product ON stock_movements (product_id)",
    ),
}

_lock = threading.Lock()
_conn: sqlite3.Connection | None = None


def _seed(conn: sqlite3.Connection) -> None:
    rng = random.Random(42)  # детерминированно: демо воспроизводимо
    cities = [(i + 1, f"Магазин №{i + 1:02d} · {CITIES[i % len(CITIES)]}") for i in range(50)]
    conn.executemany("INSERT INTO stores VALUES (?, ?)", cities)

    products = [
        (
            i + 1,
            f"MF-{i + 1:05d}",
            f"{CATEGORIES[i % len(CATEGORIES)]} {i + 1:03d}",
            CATEGORIES[i % len(CATEGORIES)],
            round(rng.uniform(9.9, 89.9), 2),
        )
        for i in range(500)
    ]
    conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)

    days = ["2026-09", "2026-10", "2026-11"]
    movements = [
        (
            rng.randint(1, 50),
            rng.randint(1, 500),
            rng.randint(1, 20),
            f"{days[rng.randint(0, 2)]}-{rng.randint(1, 28):02d}",
            rng.choice(STATUSES),
        )
        for _ in range(ROW_COUNT)
    ]
    conn.executemany(
        "INSERT INTO stock_movements (store_id, product_id, qty, moved_at, status) "
        "VALUES (?, ?, ?, ?, ?)",
        movements,
    )
    conn.commit()


def get_db() -> sqlite3.Connection:
    global _conn
    with _lock:
        if _conn is None:
            conn = sqlite3.connect(":memory:", check_same_thread=False)
            conn.executescript(
                """\
CREATE TABLE stores (store_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores (store_id),
    product_id INTEGER NOT NULL REFERENCES products (product_id),
    qty INTEGER NOT NULL,
    moved_at TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE INDEX idx_movements_status_date ON stock_movements (status, moved_at);
CREATE INDEX idx_movements_product ON stock_movements (product_id);"""
            )
            _seed(conn)
            _conn = conn
        return _conn


def _execute(conn: sqlite3.Connection, sql: str) -> tuple[list[str], list[list]]:
    cur = conn.execute(sql)
    columns = [d[0] for d in cur.description]
    return columns, [list(row) for row in cur.fetchall()]


def _plan(conn: sqlite3.Connection, sql: str) -> str:
    rows = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
    return " | ".join(r[3] for r in rows)


def run_query(query_id: str) -> dict:
    """Медленный и быстрый прогоны + планы; время меряется честно."""
    q = DEMO_QUERIES[query_id]
    conn = get_db()
    with _lock:
        t0 = time.perf_counter()
        columns, rows = _execute(conn, q.slow_sql)
        slow_ms = round((time.perf_counter() - t0) * 1000, 2)

        t0 = time.perf_counter()
        _, _ = _execute(conn, q.sql)
        fast_ms = round((time.perf_counter() - t0) * 1000, 2)

        return {
            "query_id": query_id,
            "columns": columns,
            "rows": rows,
            "slow": {"elapsed_ms": slow_ms, "plan": _plan(conn, q.slow_sql)},
            "fast": {"elapsed_ms": fast_ms, "plan": _plan(conn, q.sql)},
            "speedup": round(slow_ms / fast_ms, 1) if fast_ms > 0 else 0.0,
        }


def schema_info() -> list[dict]:
    conn = get_db()
    with _lock:
        info = []
        for name, note in TABLES:
            columns = [r[1] for r in conn.execute(f"PRAGMA table_info({name})")]
            row_count = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
            info.append({"name": name, "row_count": row_count, "columns": columns, "note": note})
        return info
