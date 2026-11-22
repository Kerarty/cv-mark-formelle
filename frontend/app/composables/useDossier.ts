/** Стор досье: MOCK по умолчанию (страница живёт без бэкенда), LIVE — по кнопке.
 *  LIVE недоступен → тихий fallback на MOCK с честным бейджем (канон №1).
 *  Всё состояние живёт в замыкании useDossier(), вызываемого в setup компонента. */

import { ENDPOINTS, MOCK } from '~/data/mock'
import type { Dossier, RunResult } from '~/types'

interface DossierState {
  mode: 'mock' | 'live'
  liveOk: boolean
  data: Dossier
  healthMs: number | null
}

const LIVE_PATHS: { key: keyof Dossier; path: string }[] = [
  { key: 'health', path: '/health' },
  { key: 'candidate', path: '/candidate' },
  { key: 'experience', path: '/experience' },
  { key: 'projects', path: '/projects' },
  { key: 'skills', path: '/skills' },
  { key: 'fit', path: '/fit' },
  { key: 'schema', path: '/sql-demo/schema' },
  { key: 'queries', path: '/sql-demo/queries' },
  { key: 'isolation', path: '/sql-demo/isolation' },
]

function delay(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms))
}

/** Детерминированные правдоподобные строки результата для мока. */
const MOCK_QUERY_ROWS: Record<string, unknown[][]> = {
  'stock-report': Array.from({ length: 12 }, (_, i) => {
    const city = ['Минск', 'Заславль', 'Брест', 'Гродно', 'Гомель', 'Витебск'][i % 6]
    const movements = 18 + ((i * 7) % 21)
    return [`Магазин №${String(i + 1).padStart(2, '0')} · ${city}`, movements, movements * (8 + ((i * 5) % 12))]
  }),
  'product-detail': Array.from({ length: 10 }, (_, i) => [
    42_000 + i * 13,
    `Магазин №${String((i % 50) + 1).padStart(2, '0')}`,
    1 + ((i * 3) % 12),
    `2026-11-${String(30 - ((i * 2) % 28)).padStart(2, '0')}`,
  ]),
}

export function useDossier() {
  const state = useState<DossierState>('dossier', () => ({
    mode: 'mock',
    liveOk: false,
    data: structuredClone(MOCK),
    healthMs: null,
  }))

  const apiBase = computed(() => useRuntimeConfig().public.apiBase as string)

  async function fetchLive(path: string, init?: RequestInit, timeoutMs = 3000): Promise<unknown> {
    const ctrl = new AbortController()
    const timer = setTimeout(() => ctrl.abort(), timeoutMs)
    try {
      const res = await fetch(apiBase.value + '/api/v1' + path, { ...init, signal: ctrl.signal })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      return await res.json()
    } finally {
      clearTimeout(timer)
    }
  }

  function mockReply(path: string): unknown {
    // значения — реактивные Proxy: structuredClone на них падает, поэтому отдаём как есть
    const d = state.value.data
    const map: Record<string, unknown> = {
      '/health': d.health,
      '/candidate': d.candidate,
      '/candidate/Kerarty': d.candidate,
      '/experience': d.experience,
      '/projects': d.projects,
      '/skills': d.skills,
      '/fit': d.fit,
      '/sql-demo/schema': d.schema,
      '/sql-demo/queries': d.queries,
      '/sql-demo/isolation': d.isolation,
    }
    if (!(path in map)) throw new Error('404')
    return map[path]
  }

  /** Один вызов для API-таба: настоящая латентность в LIVE, сдержанная симуляция в MOCK. */
  async function callEndpoint(path: string): Promise<{ ok: boolean; ms: number; body: unknown }> {
    if (state.value.mode === 'live') {
      const t0 = performance.now()
      try {
        const body = await fetchLive(path)
        return { ok: true, ms: Math.round(performance.now() - t0), body }
      } catch {
        return { ok: false, ms: Math.round(performance.now() - t0), body: { detail: 'LIVE недоступен' } }
      }
    }
    const t0 = performance.now()
    await delay(40 + Math.random() * 60)
    let ok = true
    let body: unknown
    try {
      body = mockReply(path)
    } catch {
      ok = false
      body = { detail: 'not found' }
    }
    return { ok, ms: Math.round(performance.now() - t0), body }
  }

  async function enableLive(): Promise<boolean> {
    try {
      const entries = await Promise.all(
        LIVE_PATHS.map(async ({ key, path }) => [key, await fetchLive(path)] as const),
      )
      const data = structuredClone(MOCK)
      for (const [key, value] of entries) (data as Record<string, unknown>)[key] = value
      state.value.data = data
      state.value.mode = 'live'
      state.value.liveOk = true
      return true
    } catch {
      state.value.liveOk = false
      return false
    }
  }

  function disableLive() {
    state.value.mode = 'mock'
    state.value.data = structuredClone(MOCK)
  }

  async function toggleMode() {
    if (state.value.mode === 'mock') await enableLive()
    else disableLive()
  }

  /** request-line в шапке: меряем /health — живое число вместо выдуманного. */
  async function measureHealth() {
    if (state.value.mode === 'live') {
      const t0 = performance.now()
      try {
        await fetchLive('/health')
        state.value.healthMs = Math.round(performance.now() - t0)
        state.value.liveOk = true
      } catch {
        state.value.healthMs = null
        state.value.liveOk = false
        state.value.mode = 'mock'
      }
      return
    }
    await delay(60 + Math.random() * 140)
    state.value.healthMs = 1 + Math.round(Math.random() * 3) * 7
  }

  /** SQL-демо: в LIVE — реальный прогон на 200k строк, в MOCK — симуляция около реальных значений. */
  async function runQuery(queryId: string): Promise<RunResult> {
    if (state.value.mode === 'live') {
      return (await fetchLive('/sql-demo/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query_id: queryId }),
      })) as RunResult
    }
    await delay(90 + Math.random() * 120)
    const mockBase: Record<string, { columns: string[]; slow: { elapsed_ms: number; plan: string }; fast: { elapsed_ms: number; plan: string } }> = {
      'stock-report': {
        columns: ['store', 'movements', 'total_qty'],
        slow: { elapsed_ms: 14 + Math.round(Math.random() * 50) / 10, plan: 'SCAN m | SEARCH s USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR GROUP BY | USE TEMP B-TREE FOR ORDER BY' },
        fast: { elapsed_ms: 1.4 + Math.round(Math.random() * 80) / 100, plan: 'SEARCH m USING INDEX idx_movements_status_date (status=? AND moved_at>? AND moved_at<?) | SEARCH s USING INTEGER PRIMARY KEY (rowid=?)' },
      },
      'product-detail': {
        columns: ['id', 'store', 'qty', 'moved_at'],
        slow: { elapsed_ms: 9 + Math.round(Math.random() * 40) / 10, plan: 'SCAN m | SCALAR SUBQUERY 1 | SEARCH products USING COVERING INDEX sqlite_autoindex_products_1 (sku=?)' },
        fast: { elapsed_ms: 0.3 + Math.round(Math.random() * 20) / 100, plan: 'SEARCH m USING INDEX idx_movements_product (product_id=?) | SCALAR SUBQUERY 1 | SEARCH products USING COVERING INDEX sqlite_autoindex_products_1 (sku=?)' },
      },
    }
    const base = mockBase[queryId]
    return {
      query_id: queryId,
      columns: base.columns,
      rows: MOCK_QUERY_ROWS[queryId],
      slow: base.slow,
      fast: base.fast,
      speedup: Math.round((base.slow.elapsed_ms / base.fast.elapsed_ms) * 10) / 10,
    }
  }

  return {
    mode: computed(() => state.value.mode),
    liveOk: computed(() => state.value.liveOk),
    data: computed(() => state.value.data),
    healthMs: computed(() => state.value.healthMs),
    apiBase,
    endpoints: ENDPOINTS,
    toggleMode,
    measureHealth,
    callEndpoint,
    runQuery,
  }
}
