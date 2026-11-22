<script setup lang="ts">
const { data, endpoints } = useDossier()

const stats = computed(() => [
  { label: 'эндпоинтов', value: String(endpoints.length) },
  { label: 'таблиц в демо-БД', value: String(data.value.schema.length) },
  { label: 'движений по складу', value: data.value.schema[2]?.row_count.toLocaleString('ru-RU') ?? '—' },
  { label: 'репозиториев на GitHub', value: '33' },
])
</script>

<template>
  <div>
    <div class="section">
      <div class="statrow">
        <span v-for="s in stats" :key="s.label">{{ s.label }}: <b>{{ s.value }}</b></span>
      </div>
      <p class="mono muted">
        {{ data.health.service }} v{{ data.health.version }} · кандидат представлен как микросервис: разделы — эндпоинты
      </p>
      <p>{{ data.candidate.summary }}</p>
    </div>

    <div class="section">
      <h2>$ лог опыта</h2>
      <ul class="log">
        <li v-for="e in data.experience" :key="e.title">
          <div class="period">{{ e.period }}</div>
          <div class="title">{{ e.title }}</div>
          <p class="muted" style="margin: 0">{{ e.text }}</p>
        </li>
      </ul>
    </div>

    <div class="section">
      <h2>Проекты</h2>
      <ul class="log">
        <li v-for="p in data.projects" :key="p.repo">
          <div class="title">
            <a :href="p.url" target="_blank" rel="noopener">{{ p.repo }}</a>
          </div>
          <p style="margin: 4px 0">{{ p.description }}</p>
          <p class="muted mono" style="margin: 4px 0">
            {{ p.tech.join(' · ') }}
          </p>
          <p class="muted" style="margin: 4px 0">сильная сторона: {{ p.highlight }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>
