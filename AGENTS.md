# AGENTS.md — правила работы агентов с этим репозиторием

## Проект

Интерактивное резюме-микросервис для вакансии Марк Формэль
(Python full-stack, отдел по развитию ИИ, [vacancy 139486046](https://rabota.by/vacancy/139486046)).

- `frontend/` — Nuxt 3, SSG (`nuxt generate` → GitHub Pages). Одна страница-дашборд с табами.
- `backend/` — FastAPI (Pydantic v2), SQLite для демо-SQL. Содержимое резюме — `backend/app/content.py`.

## Канон (не нарушать)

1. **Страница работает без бэкенда.** Мок-слой фронтенда всегда жив и отвечает теми же
   контрактами, что FastAPI; LIVE-режим — опция с тихим fallback на MOCK и честным бейджем.
2. **HR нельзя проиграть.** Каждый таб открывается по прямой ссылке
   (`#overview`, `#api`, `#sql`, `#ai`, `#fit`, `#honest`, `#plan`, `#contact`).
   Есть noscript-версия, print-стили, `prefers-reduced-motion`.
3. **Честность.** Маппинг требований ✓/◐/○; каждый числовой факт проверяем по
   [github.com/Kerarty](https://github.com/Kerarty); не выдумывать метрики и опыт.
   Python кандидата — университет + self-study; коммерческого опыта нет — это пишется прямо.
4. **Язык.** Пользовательские тексты — русский; идентификаторы кода — английский.
5. **Единственный источник контента** — `backend/app/content.py`. Мок-слой фронтенда
   зеркалит его ответы; при изменении эндпоинтов обновлять контракт, мок и тесты в одном коммите.

## Команды

```bash
# backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload       # Swagger: http://127.0.0.1:8000/docs
pytest                              # тесты HTTP-слоя (TestClient)
ruff check . && ruff format --check .

# frontend
cd frontend
npm ci
npm run dev                         # http://localhost:3000
npm run generate                    # статический вывод в .output/public
```

## Стиль кода

- Backend: `ruff` (lint + format), Pydantic v2 схемы для каждого ответа API.
- Тесты — по публичному HTTP-слою (`TestClient`), не по внутренностям классов.
- Минимум кода: без спекулятивных абстракций и конфигурируемости «на будущее».
- Коммиты: conventional (`feat:`, `fix:`, `test:`, `docs:`, `chore:`) — по одной фазе за коммит.

## CI/CD

Пуш в `main` → `.github/workflows/ci.yml`: ruff + pytest → npm ci + generate → deploy Pages.
`docker compose up` поднимает api + redis для проверки полного стека.
