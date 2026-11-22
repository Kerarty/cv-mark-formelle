<script setup lang="ts">
const { data } = useDossier()

/** +375447838489 → +375 44 783-84-89 — только отображение, href из данных */
const phoneView = computed(() => {
  const raw = data.value.candidate.contacts.phone ?? ''
  const m = raw.match(/^(\+375)(\d{2})(\d{3})(\d{2})(\d{2})$/)
  return m ? `${m[1]} ${m[2]} ${m[3]}-${m[4]}-${m[5]}` : raw
})
</script>

<template>
  <div>
    <div class="section">
      <h2>Этикетка изделия</h2>
      <div class="labelcard">
        <p class="tag-name">{{ data.candidate.name }}</p>
        <p class="hint" style="margin: 0 0 6px">
          досье-микросервис · GitHub-аккаунт: {{ data.candidate.handle }}
        </p>
        <Barcode />
        <div class="contactlinks">
          <a :href="data.candidate.contacts.github" target="_blank" rel="noopener"><b>github</b>github.com/Kerarty</a>
          <a :href="data.candidate.contacts.telegram" target="_blank" rel="noopener"><b>telegram</b>t.me/Kerarty</a>
          <a :href="'mailto:' + data.candidate.contacts.email"><b>email</b>{{ data.candidate.contacts.email }}</a>
          <a :href="'tel:' + data.candidate.contacts.phone"><b>phone</b>{{ phoneView }}</a>
        </div>
        <p class="hint" style="margin-bottom: 0">
          Запись на собеседование у компании — через Telegram-бот:
          <a href="https://t.me/recruit_markformelle_bot" target="_blank" rel="noopener">t.me/recruit_markformelle_bot</a>
        </p>
      </div>
    </div>
  </div>
</template>
