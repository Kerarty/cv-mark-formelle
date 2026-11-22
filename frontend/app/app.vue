<script setup lang="ts">
const { mode, liveOk, data, healthMs, endpoints, toggleMode, measureHealth } = useDossier()

const TABS = [
  { id: 'overview', num: '01', label: 'обзор' },
  { id: 'api', num: '02', label: 'api' },
  { id: 'sql', num: '03', label: 'sql' },
  { id: 'ai', num: '04', label: 'ai-конвейер' },
  { id: 'fit', num: '05', label: 'fit' },
  { id: 'honest', num: '06', label: 'честно' },
  { id: 'contact', num: '07', label: 'контакты' },
] as const

type TabId = (typeof TABS)[number]['id']

const active = ref<TabId>('overview')

function setTab(id: TabId) {
  active.value = id
  if (window.location.hash !== `#${id}`) history.replaceState(null, '', `#${id}`)
}

function tabFromHash(): TabId {
  const id = window.location.hash.slice(1) as TabId
  return TABS.some((t) => t.id === id) ? id : 'overview'
}

onMounted(() => {
  active.value = tabFromHash()
  window.addEventListener('hashchange', () => {
    active.value = tabFromHash()
  })
  measureHealth()
})

const modeLabel = computed(() =>
  mode.value === 'live' && liveOk.value ? 'LIVE' : mode.value === 'live' ? 'LIVE↓' : 'MOCK',
)

const liveHint = ref('')

async function onToggleMode() {
  const wasMock = mode.value === 'mock'
  await toggleMode()
  await measureHealth()
  if (wasMock && mode.value === 'mock' && !liveOk.value) {
    liveHint.value = 'LIVE недоступен — нет бэкенда. Страница остаётся в MOCK, всё работает.'
    setTimeout(() => (liveHint.value = ''), 4000)
  }
}

/* заголовок из единственного источника: до двоеточия — дисплейная часть;
   «full-stack» склеиваем неразрывным дефисом, чтобы не рвался на переносе */
const heroTitle = computed(() =>
  (data.value.candidate.headline.split(':')[0]?.trim() ?? '').replace('full-stack', 'full\u2011stack'),
)
const heroSub = computed(() => {
  const parts = data.value.candidate.headline.split(':')
  return parts.slice(1).join(':').trim()
})
</script>

<template>
  <div>
    <!-- noscript: все панели открыты, табы скрыты (канон №2) -->
    <noscript>
      <style>
        .panel { display: block !important; }
        .tabs, .mode { display: none !important; }
      </style>
    </noscript>

    <div class="page">
      <header class="chrome">
        <span class="chrome-brand">
          <span class="chrome-mark" aria-hidden="true">cv</span>
          <span class="chrome-path"><b>kerarty</b>/cv-mark-formelle · паспорт качества кандидата</span>
        </span>
        <button
          class="mode"
          :class="{ 'is-live': mode === 'live' && liveOk, 'is-fallback': mode === 'live' && !liveOk }"
          :title="'Переключить источник: MOCK всегда работает, LIVE ходит в реальный FastAPI (' + (mode === 'mock' ? 'включить LIVE' : 'вернуть MOCK') + ')'"
          @click="onToggleMode"
        >
          {{ modeLabel }}
        </button>
      </header>
      <p v-if="liveHint" class="hint" style="margin-top: 6px">{{ liveHint }}</p>

      <section class="hero">
        <div>
          <p class="requestline" aria-hidden="true">
            <span class="rl-method">GET</span>
            <span class="rl-url">/api/v1/candidate/{{ data.candidate.handle }}</span>
            <span class="rl-result" :class="{ ok: healthMs !== null }">
              → 200 OK<template v-if="healthMs !== null"> · {{ healthMs }} ms</template>
            </span>
            <span class="rl-cursor"></span>
          </p>
          <h1 class="display">{{ heroTitle }}</h1>
          <p class="display-sub">{{ heroSub }}</p>
          <p class="hero-note">
            Кандидат представлен как микросервис: разделы — эндпоинты, демо — испытания.
            MOCK-режим живёт без бэкенда; LIVE ходит в настоящий FastAPI — переключатель в шапке.
          </p>

          <div class="statgrid">
            <div><b>{{ endpoints.length }}</b><span>эндпоинтов досье</span></div>
            <div><b>{{ data.schema.length }}</b><span>таблиц в демо-БД</span></div>
            <div><b>{{ data.schema[2]?.row_count.toLocaleString('ru-RU') ?? '—' }}</b><span>движений по складу</span></div>
            <div><b>{{ data.candidate.public_repos }}</b><span>репозиториев на GitHub</span></div>
          </div>
        </div>

        <aside class="tag" aria-label="Бирка изделия: досье кандидата">
          <span class="tag-hole" aria-hidden="true"></span>
          <p class="tag-name">{{ data.candidate.name }}</p>
          <p class="tag-role">{{ data.candidate.handle }} · досье-микросервис · интерактивное резюме</p>
          <Barcode />
          <p class="tag-made">сделано конвейером ai-ассистентов</p>
          <p class="tag-geo">
            <span>Минск · Беларусь</span>
            <span>изделие №2026</span>
          </p>
        </aside>
      </section>

      <div class="swatches" aria-hidden="true">
        <span>коллекция</span>
        <i style="background: var(--yarn-sage)"></i>
        <i style="background: var(--yarn-sky)"></i>
        <i style="background: var(--yarn-rose)"></i>
        <i style="background: var(--yarn-sand)"></i>
        <i style="background: var(--yarn-melange)"></i>
        <i style="background: var(--yarn-denim)"></i>
      </div>

      <nav class="tabs" role="tablist" aria-label="Разделы досье">
        <button
          v-for="t in TABS"
          :key="t.id"
          class="tab"
          role="tab"
          :aria-selected="active === t.id"
          @click="setTab(t.id)"
        >
          <i aria-hidden="true">{{ t.num }}</i>{{ t.label }}
        </button>
      </nav>

      <main>
        <section v-show="active === 'overview'" id="overview" class="panel" role="tabpanel" aria-label="обзор">
          <OverviewTab />
        </section>
        <section v-show="active === 'api'" id="api" class="panel" role="tabpanel" aria-label="api">
          <ApiTab />
        </section>
        <section v-show="active === 'sql'" id="sql" class="panel" role="tabpanel" aria-label="sql">
          <SqlTab />
        </section>
        <section v-show="active === 'ai'" id="ai" class="panel" role="tabpanel" aria-label="ai-конвейер">
          <AiTab />
        </section>
        <section v-show="active === 'fit'" id="fit" class="panel" role="tabpanel" aria-label="fit">
          <FitTab />
        </section>
        <section v-show="active === 'honest'" id="honest" class="panel" role="tabpanel" aria-label="честно">
          <HonestTab />
        </section>
        <section v-show="active === 'contact'" id="contact" class="panel" role="tabpanel" aria-label="контакты">
          <ContactTab />
        </section>
      </main>
    </div>

    <footer class="footband">
      <div class="footband-in">
        <div>
          <p class="big">Каждый числовой факт проверяем по <a href="https://github.com/Kerarty" target="_blank" rel="noopener">github.com/Kerarty</a></p>
          <p class="small">
            собрано конвейером Claude Code · FastAPI + Pydantic v2 + Nuxt 3 (SSG) · тесты HTTP-слоя в CI
          </p>
        </div>
        <div>
          <Barcode />
          <p class="small" style="margin-top: 8px">kerarty.github.io/cv-mark-formelle</p>
        </div>
      </div>
    </footer>
  </div>
</template>
