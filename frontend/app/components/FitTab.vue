<script setup lang="ts">
const { data } = useDossier()
</script>

<template>
  <div>
    <div class="section">
      <h2>Маппинг требований вакансии на доказательства</h2>
      <p class="hint">✓ есть — демонстрируется в этом проекте или репозитории; ◐ частично — есть база, нет боя; ○ план — закрываю после выхода в роль.</p>
      <div v-for="f in data.fit" :key="f.requirement" class="fit-item">
        <div><StatusBadge :status="f.status" /></div>
        <div>
          <div class="req">{{ f.requirement }}</div>
          <p class="muted" style="margin: 0">{{ f.evidence }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
