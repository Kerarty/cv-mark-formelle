<script setup lang="ts">
const { data } = useDossier()
</script>

<template>
  <div>
    <div class="section">
      <h2>Паспорт изделия</h2>
      <p class="muted mono" style="margin-top: 0">
        {{ data.health.service }} v{{ data.health.version }} · отдел техконтроля: тесты HTTP-слоя
      </p>
      <p style="font-size: 17px; max-width: 62ch">{{ data.candidate.summary }}</p>
    </div>

    <div class="section">
      <h2>Опыт: хронология нити</h2>
      <ul class="xp">
        <li v-for="e in data.experience" :key="e.title">
          <div class="period">{{ e.period }}</div>
          <div class="title">{{ e.title }}</div>
          <p class="muted" style="margin: 4px 0 0; font-size: 14.5px">{{ e.text }}</p>
        </li>
      </ul>
    </div>

    <div class="section">
      <h2>Изделия: репозитории</h2>
      <div class="cards">
        <a v-for="p in data.projects" :key="p.repo" class="card" :href="p.url" target="_blank" rel="noopener">
          <p class="card-title"><span class="mono">{{ p.repo }}</span> ↗</p>
          <p>{{ p.description }}</p>
          <div class="techrow">
            <span v-for="t in p.tech" :key="t" class="chip">{{ t }}</span>
          </div>
          <p class="muted" style="margin-top: 10px"><b style="color: var(--ink)">сильная сторона:</b> {{ p.highlight }}</p>
        </a>
      </div>
    </div>
  </div>
</template>
