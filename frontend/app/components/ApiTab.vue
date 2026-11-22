<script setup lang="ts">
const { mode, apiBase, callEndpoint, endpoints } = useDossier()

const result = ref<{ path: string; ok: boolean; ms: number; body: unknown } | null>(null)
const loading = ref('')

async function run(path: string) {
  loading.value = path
  result.value = null
  const r = await callEndpoint(path)
  result.value = { path, ...r }
  loading.value = ''
}
</script>

<template>
  <div>
    <div class="section">
      <h2>Эндпоинты досье</h2>
      <p class="hint">
        Клик по строке выполняет запрос — латентность настоящая. POST /sql-demo/run живёт в табе
        <a href="#sql">sql</a>.
        <template v-if="mode === 'live'">
          Swagger: <a :href="apiBase + '/docs'" target="_blank" rel="noopener">{{ apiBase }}/docs</a>
        </template>
        <template v-else>
          В MOCK-режиме ответы отдаются из мок-слоя; включи LIVE, чтобы дёргать реальный FastAPI.
        </template>
      </p>
      <div class="tscroll">
        <table class="ep-table">
        <tbody>
          <tr
            v-for="ep in endpoints"
            :key="ep.path"
            :class="{ endpoint: ep.method === 'GET' }"
            :tabindex="ep.method === 'GET' ? 0 : -1"
            :role="ep.method === 'GET' ? 'button' : undefined"
            @click="ep.method === 'GET' && run(ep.path)"
            @keydown.enter="ep.method === 'GET' && run(ep.path)"
          >
            <td><span class="method" :class="ep.method.toLowerCase()">{{ ep.method }}</span></td>
            <td class="mono">{{ ep.path }}</td>
            <td class="muted">{{ ep.note }}</td>
          </tr>
        </tbody>
        </table>
      </div>
      <p v-if="loading" class="mono muted">… выполняется {{ loading }}</p>
      <template v-if="result">
        <p class="mono">
          {{ result.path }} → {{ result.ok ? '200 OK' : 'ERROR' }} · {{ result.ms }} ms
        </p>
        <JsonView :value="result.body" />
      </template>
    </div>
  </div>
</template>
