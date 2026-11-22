from typing import Literal

from pydantic import BaseModel


class Health(BaseModel):
    status: str
    service: str
    version: str


class Vacancy(BaseModel):
    company: str
    title: str
    rabota_id: int
    url: str


class Contacts(BaseModel):
    github: str
    telegram: str | None = None
    email: str | None = None


class Candidate(BaseModel):
    handle: str
    headline: str
    summary: str
    contacts: Contacts
    vacancy: Vacancy


class LogEntry(BaseModel):
    period: str
    title: str
    text: str


class Project(BaseModel):
    repo: str
    url: str
    description: str
    tech: list[str]
    highlight: str


class Skills(BaseModel):
    proven: list[str]
    partial: list[str]
    plan: list[str]


FitStatus = Literal["full", "partial", "plan"]


class FitItem(BaseModel):
    requirement: str
    status: FitStatus
    evidence: str


class TableInfo(BaseModel):
    name: str
    row_count: int
    columns: list[str]
    note: str


class DemoQuery(BaseModel):
    id: str
    title: str
    description: str
    tsql: str
    sql: str
    index_name: str
    index_sql: str


class RunRequest(BaseModel):
    query_id: str


class PlanRun(BaseModel):
    elapsed_ms: float
    plan: str


class RunResult(BaseModel):
    query_id: str
    columns: list[str]
    rows: list[list]
    slow: PlanRun
    fast: PlanRun
    speedup: float


class IsolationScenario(BaseModel):
    anomaly: str
    note: str
    tsql: str
