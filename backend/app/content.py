"""Кандидат — единственный источник контента резюме (канон №5 из AGENTS.md).

Все числовые факты проверяемы по github.com/Kerarty.
Значения ``None`` в контактах — заполняются перед финальным деплоем.
"""

CANDIDATE = {
    "handle": "Kerarty",
    "headline": "Python-разработчик (full-stack): резюме, которое само работает на FastAPI + Nuxt",
    "summary": (
        "Университетский Python + self-study. Собираю рабочие продукты конвейером "
        "AI-ассистентов: от SDK playable-рекламы до этого досье, которое отвечает "
        "REST-эндпоинтами. Вакансия просит FastAPI, Nuxt и SQL — все три здесь, в бою."
    ),
    "contacts": {
        "github": "https://github.com/Kerarty",
        "telegram": None,
        "email": None,
    },
    "vacancy": {
        "company": "Марк Формэль",
        "title": "Python-разработчик (Full-stack), отдел по развитию ИИ",
        "rabota_id": 139486046,
        "url": "https://rabota.by/vacancy/139486046?hhtmFrom=favorites",
    },
}

# $ лог опыта: каждый факт проверяем по датам создания репозиториев (api.github.com/Kerarty)
EXPERIENCE = [
    {
        "period": "2024 — н.в.",
        "title": "БГУИР: университетский Python + self-study",
        "text": (
            "Python — университетский курс плюс самостоятельное углубление: практика на "
            "скриптах, REST-клиентах и малых сервисах. Коммерческого опыта пока нет — "
            "это написано прямо."
        ),
    },
    {
        "period": "2026.10.05",
        "title": "playable-реклама: SDK + два играбельных ролика за день релиза",
        "text": (
            "playble-ads — движко-независимый SDK с адаптерами рекламных сетей; "
            "playable-ad-mob-rush — crowd runner на PixiJS, вся игра в одном HTML-файле "
            "472 КБ с процедурным арт и звуком, поддержка MRAID."
        ),
    },
    {
        "period": "2026.10 — 2026.11",
        "title": "20 интерактивных резюме за ~6 недель, конвейером AI-ассистентов",
        "text": (
            "Серия cv-* репозиториев с 06.10 по 19.11.2026 — один самостоятельный "
            "продукт на вакансию с живой механикой под её контекст. AGENTS.md-правила, "
            "субагенты, проверка фактов — навык ежедневной работы с ассистентами."
        ),
    },
    {
        "period": "2026.11.15",
        "title": "hsm-qa-scripts: Python-клиент REST API (QA-задание SoftFx)",
        "text": (
            "Скрипт отправки данных датчиков в HSM REST API — реальная работа с HTTP, "
            "сериализацией и обработкой ответов."
        ),
    },
    {
        "period": "2026.11.22",
        "title": "cv-mark-formelle — это резюме: FastAPI + Nuxt + SQL-демо",
        "text": (
            "Ответ на вакансию Марк Формэль: бэкенд на FastAPI с Pydantic v2 и тестами, "
            "фронтенд на Nuxt 3, SQL-консоль с оптимизацией запросов на 200k строк."
        ),
    },
]

PROJECTS = [
    {
        "repo": "cv-mark-formelle",
        "url": "https://github.com/Kerarty/cv-mark-formelle",
        "description": (
            "Это резюме: дашборд «кандидат как микросервис» — FastAPI, Nuxt 3, "
            "SQL-консоль с EXPLAIN, docker-compose, CI, тесты."
        ),
        "tech": [
            "Python",
            "FastAPI",
            "Pydantic v2",
            "Nuxt 3",
            "SQLite",
            "Docker",
            "GitHub Actions",
        ],
        "highlight": "двухрежимный API: страница живёт без бэкенда, LIVE — по кнопке",
    },
    {
        "repo": "playble-ads",
        "url": "https://github.com/Kerarty/playble-ads",
        "description": (
            "Движко-независимый SDK для HTML5 playable-рекламы с адаптерами под "
            "основные рекламные сети."
        ),
        "tech": ["TypeScript", "HTML5", "MRAID"],
        "highlight": "архитектура адаптеров поверх одного ядра",
    },
    {
        "repo": "playable-ad-mob-rush",
        "url": "https://github.com/Kerarty/playable-ad-mob-rush",
        "description": (
            "Crowd runner на PixiJS: вся игра в одном HTML-файле 472 КБ — процедурный "
            "арт и звук вместо ассетов, интеграция MRAID."
        ),
        "tech": ["JavaScript", "PixiJS 8", "Web Audio", "MRAID"],
        "highlight": "472 КБ, ноль внешних запросов",
    },
    {
        "repo": "echoloop-playble",
        "url": "https://github.com/Kerarty/echoloop-playble",
        "description": (
            "Головоломка о времени на Unity 6 + URP: петля уровня, эхо прошлых "
            "проходов игрока, 8 уровней."
        ),
        "tech": ["C#", "Unity 6", "URP"],
        "highlight": "механика «эха» как единственный ход головоломки",
    },
    {
        "repo": "cv-zhuk",
        "url": "https://github.com/Kerarty/cv-zhuk",
        "description": (
            "Резюме-харнес для вакансии Python/AI: страница — сессия агента, который "
            "собирает досье у HR на глазах; 49 субагентов, 107 скиллов в конвейере."
        ),
        "tech": ["HTML", "JavaScript", "AI-конвейер"],
        "highlight": "форма отвечает содержанию: работа с агентами показана, не заявлена",
    },
    {
        "repo": "hsm-qa-scripts",
        "url": "https://github.com/Kerarty/hsm-qa-scripts",
        "description": (
            "QA-задание SoftFx: Python-скрипт отправки данных датчиков в HSM REST API."
        ),
        "tech": ["Python", "REST API", "HTTP"],
        "highlight": "первый проверяемый Python-артефакт вне университета",
    },
]

SKILLS = {
    "proven": [
        "TypeScript / JavaScript",
        "PixiJS 8 · HTML5-игры",
        "Unity 6 + C#",
        "HTML / CSS",
        "AI-конвейер: Claude Code, AGENTS.md, субагенты",
        "Git",
    ],
    "partial": [
        "Python — университет + self-study, реальные скрипты",
        "SQL — индексы, JOIN, изоляция: теория + демо этого проекта",
        "FastAPI — REST API этого проекта",
        "Nuxt 3 — фронтенд этого проекта",
        "Docker / CI — compose и Actions этого проекта",
        "Redis — в docker-compose этого проекта",
    ],
    "plan": [
        "MS SQL Server в бою",
        "ClickHouse",
        "RabbitMQ",
        "Мониторинг: Zabbix / ELK / Sentry",
        "Telegram-боты + интеграция LLM",
    ],
}

FIT = [
    {
        "requirement": "AI-инструменты: Cursor / Claude Code / Copilot ежедневно",
        "status": "full",
        "evidence": (
            "Конвейер на Claude Code: AGENTS.md с правилами, субагенты, факт-чек. "
            "20+ продуктов за 6 недель — проверяемо по датам создания репозиториев."
        ),
    },
    {
        "requirement": "SQL (MS SQL Server): индексы, JOIN, транзакции, изоляция",
        "status": "partial",
        "evidence": (
            "Демо в этом проекте: план запроса до/после индекса на 200k строк, "
            "разбор изоляции. Боевого MS SQL Server нет — закрываю практикой "
            "в первые месяцы работы."
        ),
    },
    {
        "requirement": "Python: ООП, чтение чужого кода, рефакторинг",
        "status": "partial",
        "evidence": (
            "Университетский курс + self-study; hsm-qa-scripts (REST-клиент). "
            "Коммерческого опыта нет — сказано прямо."
        ),
    },
    {
        "requirement": "FastAPI: REST API, Pydantic, async, микросервисы",
        "status": "partial",
        "evidence": (
            "Бэкенд этого проекта: роутинг, Pydantic v2 схемы, тесты HTTP-слоя, "
            "Swagger. Коммерческого опыта нет."
        ),
    },
    {
        "requirement": "Nuxt / Vue: самостоятельный фронтенд своих сервисов",
        "status": "partial",
        "evidence": (
            "Дашборд этого проекта собран на Nuxt 3 (SSG). До этого — 20+ "
            "интерфейсов на чистом JS/Canvas."
        ),
    },
    {
        "requirement": "+ Docker, CI/CD, GitLab",
        "status": "partial",
        "evidence": "docker-compose (api + redis) и GitHub Actions CI в этом репо.",
    },
    {
        "requirement": "+ RabbitMQ, Redis, ClickHouse, мониторинг, Telegram-боты и LLM",
        "status": "plan",
        "evidence": (
            "Redis — в compose проекта; по остальному — конкретные первые задачи "
            "в отделе ИИ, готов расписать на собеседовании."
        ),
    },
]

# Уровни изоляции MS SQL Server на ритейл-сценариях остатков
ISOLATION = [
    {
        "anomaly": "Потерянное обновление (lost update)",
        "note": (
            "Два кассира одновременно резервируют последний остаток; второй UPDATE "
            "перезаписывает первый — продано два, на складе один. READ COMMITTED не "
            "спасает: нужна блокировка читаемой строки."
        ),
        "tsql": """\
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN TRANSACTION;
  SELECT qty FROM stock WHERE sku = 'MF-00042' WITH (UPDLOCK, ROWLOCK);
  -- проверка остатка и списание
  UPDATE stock SET qty = qty - 1 WHERE sku = 'MF-00042';
COMMIT;""",
    },
    {
        "anomaly": "Неповторяющееся чтение (non-repeatable read)",
        "note": (
            "Отчёт по остаткам читает строку дважды, между чтениями соседняя "
            "транзакция списала товар — итоги отчёта разъехались. Лечится "
            "REPEATABLE READ: разделяемые блокировки держатся до конца транзакции."
        ),
        "tsql": """\
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

BEGIN TRANSACTION;
  SELECT SUM(qty) FROM stock WHERE store_id = 7;
  -- соседняя UPDATE по этим строкам ждёт нашей COMMIT
  SELECT SUM(qty) FROM stock WHERE store_id = 7;  -- то же значение
COMMIT;""",
    },
    {
        "anomaly": "Фантомное чтение (phantom read)",
        "note": (
            "Отчёт отбирает отгрузки за смену; в середине запроса приходит новая "
            "отгрузка и попадает во вторую выборку — «фантом». REPEATABLE READ "
            "блокирует существующие строки, но не новые; нужен SERIALIZABLE/HOLDLOCK."
        ),
        "tsql": """\
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN TRANSACTION;
  SELECT COUNT(*) FROM stock_movements
  WHERE moved_at >= '2026-11-22' AND status = 'shipped';  -- 148
  -- новая отгрузка со стороны ждёт COMMIT
  SELECT COUNT(*) FROM stock_movements
  WHERE moved_at >= '2026-11-22' AND status = 'shipped';  -- снова 148
COMMIT;""",
    },
    {
        "anomaly": "Взаимная блокировка (deadlock)",
        "note": (
            "Сервис остатков лочит товар и берёт движение; сервис отчётов лочит "
            "движение и берёт товар — оба ждут друг друга. Лечение: единый порядок "
            "доступа к таблицам и короткие транзакции; в MS SQL ловим ошибку 1205."
        ),
        "tsql": """\
-- оба сервиса: всегда сначала stock, потом stock_movements
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN TRY
  BEGIN TRANSACTION;
    UPDATE stock SET qty = qty - 1 WHERE sku = 'MF-00042';
    INSERT INTO stock_movements (...) VALUES (...);
  COMMIT;
END TRY
BEGIN CATCH
  IF ERROR_NUMBER() = 1205 ROLLBACK;  -- deadlock victim: повторить
  THROW;
END CATCH;""",
    },
]
