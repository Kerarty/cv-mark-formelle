"""Seam: SQL-демо — схема ритейла, запросы с планами, изоляция."""


def test_schema_of_retail_demo(client):
    r = client.get("/api/v1/sql-demo/schema")
    assert r.status_code == 200
    tables = {t["name"]: t for t in r.json()}
    assert set(tables) == {"stores", "products", "stock_movements"}
    assert tables["stock_movements"]["row_count"] == 200_000
    assert "store_id" in tables["stock_movements"]["columns"]


def test_demo_queries_registry(client):
    r = client.get("/api/v1/sql-demo/queries")
    assert r.status_code == 200
    queries = {q["id"]: q for q in r.json()}
    assert set(queries) == {"stock-report", "product-detail"}
    for q in queries.values():
        # T-SQL витрина для HR и исполняемый SQLite-вариант для демо
        assert "SELECT" in q["tsql"].upper()
        assert "SELECT" in q["sql"].upper()
        assert q["index_sql"].upper().startswith("CREATE")
        assert len(q["description"]) > 0


def test_run_shows_slow_vs_fast(client):
    r = client.post("/api/v1/sql-demo/run", json={"query_id": "stock-report"})
    assert r.status_code == 200
    body = r.json()

    assert body["query_id"] == "stock-report"
    assert len(body["columns"]) >= 2
    assert len(body["rows"]) > 0
    # медленный прогон — полный скан, быстрый — поиск по индексу
    assert "SCAN" in body["slow"]["plan"]
    assert "INDEX" in body["fast"]["plan"]
    assert body["fast"]["elapsed_ms"] < body["slow"]["elapsed_ms"]
    assert body["speedup"] >= 2.0


def test_run_product_detail(client):
    r = client.post("/api/v1/sql-demo/run", json={"query_id": "product-detail"})
    assert r.status_code == 200
    body = r.json()
    assert body["speedup"] >= 2.0
    assert len(body["rows"]) > 0


def test_run_unknown_query_and_validation(client):
    r = client.post("/api/v1/sql-demo/run", json={"query_id": "no-such-query"})
    assert r.status_code == 404

    r = client.post("/api/v1/sql-demo/run", json={})
    assert r.status_code == 422


def test_isolation_scenarios(client):
    r = client.get("/api/v1/sql-demo/isolation")
    assert r.status_code == 200
    scenarios = r.json()
    assert len(scenarios) >= 3
    for s in scenarios:
        assert set(s) >= {"anomaly", "note", "tsql"}
        assert "SET TRANSACTION ISOLATION LEVEL" in s["tsql"]
