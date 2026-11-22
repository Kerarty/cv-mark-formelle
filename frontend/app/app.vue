<script setup lang="ts">
const { mode, liveOk, data, healthMs, toggleMode, measureHealth } = useDossier()

const TABS = [
  { id: 'overview', label: 'обзор' },
  { id: 'api', label: 'api' },
  { id: 'sql', label: 'sql' },
  { id: 'ai', label: 'ai-конвейер' },
  { id: 'fit', label: 'fit' },
  { id: 'honest', label: 'честно' },
  { id: 'contact', label: 'контакты' },
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
</script>

<template>
  <div class="page">
    <!-- noscript: все панели открыты, табы скрыты (канон №2) -->
    <noscript>
      <style>
        .panel { display: block !important; }
        .tabs, .mode { display: none !important; }
      </style>
    </noscript>

    <header class="chrome">
      <span>cv-mark-formelle</span>
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

    <div class="requestline" aria-hidden="true">
      <span class="rl-method">GET</span>
      <span class="rl-url">/api/v1/candidate/{{ data.candidate.handle }}</span>
      <span class="rl-result" :class="{ ok: healthMs !== null }">
        → 200 OK<template v-if="healthMs !== null"> · {{ healthMs }} ms</template>
      </span>
    </div>
    <p class="headline">{{ data.candidate.headline }}</p>

    <nav class="tabs" role="tablist" aria-label="Разделы досье">
      <button
        v-for="t in TABS"
        :key="t.id"
        class="tab"
        role="tab"
        :aria-selected="active === t.id"
        @click="setTab(t.id)"
      >
        {{ t.label }}
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

    <footer class="foot">
      github.com/Kerarty · каждый числовой факт проверяем по репозиториям · собрано конвейером Claude Code
    </footer>
  </div>
</template>
