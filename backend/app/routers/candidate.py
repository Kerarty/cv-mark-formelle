from fastapi import APIRouter, HTTPException

from app import content, meta
from app.schemas import Candidate, FitItem, Health, LogEntry, Project, Skills

router = APIRouter()


@router.get("/health", response_model=Health)
def health() -> Health:
    return Health(status="ok", service=meta.SERVICE_NAME, version=meta.APP_VERSION)


@router.get("/candidate", response_model=Candidate)
def candidate() -> Candidate:
    return Candidate(**content.CANDIDATE)


@router.get("/candidate/{handle}", response_model=Candidate)
def candidate_by_handle(handle: str) -> Candidate:
    if handle != content.CANDIDATE["handle"]:
        raise HTTPException(status_code=404, detail=f"Кандидат «{handle}» не найден")
    return Candidate(**content.CANDIDATE)


@router.get("/experience", response_model=list[LogEntry])
def experience() -> list[LogEntry]:
    return [LogEntry(**e) for e in content.EXPERIENCE]


@router.get("/projects", response_model=list[Project])
def projects() -> list[Project]:
    return [Project(**p) for p in content.PROJECTS]


@router.get("/skills", response_model=Skills)
def skills() -> Skills:
    return Skills(**content.SKILLS)


@router.get("/fit", response_model=list[FitItem])
def fit() -> list[FitItem]:
    return [FitItem(**f) for f in content.FIT]
