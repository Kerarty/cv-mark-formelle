"""Seam: контент резюме — опыт, проекты, навыки, маппинг на вакансию."""

REPOS = {"playble-ads", "echoloop-playble", "playable-ad-mob-rush", "cv-zhuk", "hsm-qa-scripts"}


def test_experience_log(client):
    r = client.get("/api/v1/experience")
    assert r.status_code == 200
    entries = r.json()
    assert isinstance(entries, list) and len(entries) >= 4
    for e in entries:
        assert set(e) >= {"period", "title", "text"}
        assert all(e[k] for k in ("period", "title", "text"))
    # университетский Python — заявлен честно, в начале лога
    joined = " ".join(e["title"] + e["text"] for e in entries).lower()
    assert "python" in joined


def test_projects_are_real_repos(client):
    r = client.get("/api/v1/projects")
    assert r.status_code == 200
    projects = r.json()
    assert isinstance(projects, list) and len(projects) >= 4
    for p in projects:
        assert set(p) >= {"repo", "url", "description", "tech"}
        assert p["url"].startswith("https://github.com/Kerarty/")
    repos = {p["repo"] for p in projects}
    assert repos >= REPOS  # каждый заявленный проект существует


def test_skills_groups(client):
    r = client.get("/api/v1/skills")
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"proven", "partial", "plan"}
    assert body["proven"] and body["partial"] and body["plan"]
    # честность: Python и FastAPI не заявлены как proven
    assert "Python" not in body["proven"]
    assert any("Python" in s for s in body["partial"])
    assert any("MS SQL" in s for s in body["plan"])


def test_fit_maps_vacancy_requirements(client):
    r = client.get("/api/v1/fit")
    assert r.status_code == 200
    fit = r.json()
    statuses = {item["requirement"]: item["status"] for item in fit}
    for item in fit:
        assert item["status"] in {"full", "partial", "plan"}
        assert len(item["evidence"]) > 0
    # ключевые требования вакансии присутствуют
    assert any("SQL" in req for req in statuses)
    assert any("Python" in req for req in statuses)
    assert any("FastAPI" in req for req in statuses)
    assert any("Nuxt" in req for req in statuses)
    assert any("AI" in req for req in statuses)
    # AI-инструменты — единственный статус full: конвейер виден в репо
    ai_req = next(req for req in statuses if "AI" in req)
    assert statuses[ai_req] == "full"
    # SQL не заявлен как full — боевого MS SQL нет
    sql_req = next(req for req in statuses if "SQL" in req)
    assert statuses[sql_req] != "full"
