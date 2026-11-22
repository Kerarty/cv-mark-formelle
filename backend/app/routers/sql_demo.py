from fastapi import APIRouter, HTTPException

from app import content, retail_db
from app.retail_db import DEMO_QUERIES
from app.schemas import (
    DemoQuery,
    IsolationScenario,
    RunRequest,
    RunResult,
    TableInfo,
)

router = APIRouter()


@router.get("/schema", response_model=list[TableInfo])
def schema() -> list[TableInfo]:
    return [TableInfo(**t) for t in retail_db.schema_info()]


@router.get("/queries", response_model=list[DemoQuery])
def queries() -> list[DemoQuery]:
    return [
        DemoQuery(
            id=q.id,
            title=q.title,
            description=q.description,
            tsql=q.tsql,
            sql=q.sql,
            index_name=q.index_name,
            index_sql=q.index_sql,
        )
        for q in DEMO_QUERIES.values()
    ]


@router.post("/run", response_model=RunResult)
def run(req: RunRequest) -> RunResult:
    if req.query_id not in DEMO_QUERIES:
        raise HTTPException(status_code=404, detail=f"Демо-запрос «{req.query_id}» не найден")
    return RunResult(**retail_db.run_query(req.query_id))


@router.get("/isolation", response_model=list[IsolationScenario])
def isolation() -> list[IsolationScenario]:
    return [IsolationScenario(**s) for s in content.ISOLATION]
