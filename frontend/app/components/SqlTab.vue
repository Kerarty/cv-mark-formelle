<script setup lang="ts">
const { mode, data, runQuery } = useDossier()

const result = ref<RunResult | null>(null)
const running = ref('')
const error = ref('')

async function run(queryId: string) {
  running.value = queryId
  error.value = ''
  result.value = null
  try {
    result.value = await runQuery(queryId)
  } catch {
    error.value = 'LIVE-бэкенд недоступен: подними его (docker compose up) или верни MOCK.'
  }
  running.value = ''
}
</script>

<template>
  <div>
    <div class="section">
      <h2>Схема демо — витрина ритейла</h2>
      <p class="hint">
        SQLite-зеркало склада с честными планами запросов; витрины T-SQL — в том виде, в котором
        запросы живут в MS SQL Server.
        <template v-if="mode === 'live'"> Сейчас LIVE: прогоны считаются на настоящем бэкенде.</template>
        <template v-else> Сейчас MOCK: числа — симуляция около измеренных на бэкенде значений.</template>
      </p>
      <table>
        <thead>
          <tr>
            <th>таблица</th>
            <th>строк</th>
            <th>колонки</th>
            <th>зачем в демо</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in data.schema" :key="t.name">
            <td class="mono">{{ t.name }}</td>
            <td class="num">{{ t.row_count.toLocaleString('ru-RU') }}</td>
            <td class="mono muted">{{ t.columns.join(', ') }}</td>
            <td class="muted">{{ t.note }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="section">
      <h2>Демо-запросы: медленный и быстрый прогоны</h2>
      <div v-for="q in data.queries" :key="q.id" style="padding: 14px 0; border-bottom: 1px solid var(--line)">
        <h3 style="margin-top: 0">{{ q.title }}</h3>
        <p style="margin-top: 0">{{ q.description }}</p>
        <CodeBlock :code="q.tsql" />
        <p class="hint">SQLite-вариант, исполняемый бэкендом: {{ q.index_name }}</p>
        <button class="btn" :disabled="running === q.id" @click="run(q.id)">
          {{ running === q.id ? '… идёт прогон' : 'Запустить сравнение' }}
        </button>
        <template v-if="result && result.query_id === q.id">
          <RunPanel :result="result" />
        </template>
      </div>
      <p v-if="error" class="mono" style="color: var(--mid)">{{ error }}</p>
    </div>

    <div class="section">
      <h2>Транзакции и уровни изоляции — на остатках склада</h2>
      <div v-for="s in data.isolation" :key="s.anomaly" style="padding: 14px 0; border-bottom: 1px solid var(--line)">
        <h3 style="margin-top: 0">{{ s.anomaly }}</h3>
        <p style="margin-top: 0">{{ s.note }}</p>
        <CodeBlock :code="s.tsql" />
      </div>
    </div>
  </div>
</template>
