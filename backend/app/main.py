from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import meta
from app.routers import candidate, sql_demo

# локальный Nuxt dev-сервер и GitHub Pages, откуда ходит LIVE-режим
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://kerarty.github.io",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="CV Mark Formelle — отдел по развитию ИИ",
        description=(
            "Досье кандидата как REST API. Pydantic v2, SQLite-демо ритейл-схемы. "
            "Страница резюме — kerarty.github.io/cv-mark-formelle."
        ),
        version=meta.APP_VERSION,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        # локальная проверка LIVE-режима с любого dev-порта (3000, 8077, ...)
        allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.include_router(candidate.router, prefix="/api/v1")
    app.include_router(sql_demo.router, prefix="/api/v1/sql-demo", tags=["sql-demo"])
    return app


app = create_app()
