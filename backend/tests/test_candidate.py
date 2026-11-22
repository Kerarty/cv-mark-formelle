"""Seam: health-check и досье кандидата (публичный HTTP-слой)."""


def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "cv-mark-formelle"


def test_candidate_returns_dossier(client):
    r = client.get("/api/v1/candidate")
    assert r.status_code == 200
    body = r.json()

    assert body["handle"] == "Kerarty"
    assert body["contacts"]["github"].startswith("https://github.com/Kerarty")
    assert isinstance(body["headline"], str) and len(body["headline"]) > 0
    # публичные репозитории — проверяемое число с api.github.com/users/Kerarty
    assert isinstance(body["public_repos"], int) and body["public_repos"] >= 30
    assert body["vacancy"]["company"] == "Марк Формэль"
    assert body["vacancy"]["rabota_id"] == 139486046


def test_candidate_by_handle_and_unknown_404(client):
    r = client.get("/api/v1/candidate/Kerarty")
    assert r.status_code == 200
    assert r.json()["handle"] == "Kerarty"

    r = client.get("/api/v1/candidate/nobody")
    assert r.status_code == 404
    assert "detail" in r.json()
