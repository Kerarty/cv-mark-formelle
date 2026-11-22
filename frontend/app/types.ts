/** Типы — зеркала Pydantic-схем бэкенда (backend/app/schemas.py). */

export interface Health {
  status: string
  service: string
  version: string
}

export interface Candidate {
  handle: string
  headline: string
  summary: string
  public_repos: number
  contacts: { github: string; telegram: string | null; email: string | null }
  vacancy: { company: string; title: string; rabota_id: number; url: string }
}

export interface LogEntry {
  period: string
  title: string
  text: string
}

export interface Project {
  repo: string
  url: string
  description: string
  tech: string[]
  highlight: string
}

export interface Skills {
  proven: string[]
  partial: string[]
  plan: string[]
}

export type FitStatus = 'full' | 'partial' | 'plan'

export interface FitItem {
  requirement: string
  status: FitStatus
  evidence: string
}

export interface TableInfo {
  name: string
  row_count: number
  columns: string[]
  note: string
}

export interface DemoQuery {
  id: string
  title: string
  description: string
  tsql: string
  sql: string
  index_name: string
  index_sql: string
}

export interface PlanRun {
  elapsed_ms: number
  plan: string
}

export interface RunResult {
  query_id: string
  columns: string[]
  rows: unknown[][]
  slow: PlanRun
  fast: PlanRun
  speedup: number
}

export interface IsolationScenario {
  anomaly: string
  note: string
  tsql: string
}

/** Всё, что отдаёт досье — мок или живой API. */
export interface Dossier {
  health: Health
  candidate: Candidate
  experience: LogEntry[]
  projects: Project[]
  skills: Skills
  fit: FitItem[]
  schema: TableInfo[]
  queries: DemoQuery[]
  isolation: IsolationScenario[]
}
