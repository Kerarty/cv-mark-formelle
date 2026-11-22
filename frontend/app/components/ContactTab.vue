<script setup lang="ts">
const { data } = useDossier()

const PITCH = `Здравствуйте! Откликаюсь на «Python-разработчик (Full-stack)» в отдел по развитию ИИ Марк Формэль. Резюме собрал как работающий микросервис: FastAPI + Pydantic v2 с тестами HTTP-слоя, фронтенд на Nuxt 3, SQL-демо с планами до/после индекса на 200k строк — kerarty.github.io/cv-mark-formelle (репо: github.com/Kerarty/cv-mark-formelle). Стек вакансии показал в работающем коде, а не в списке навыков. AI-ассистентами пользуюсь ежедневно — конвейер открыт в AGENTS.md. Честно: коммерческого Python пока нет — университетский курс + self-study; как закрою этот разрыв — готов показать на собеседовании.`

const copied = ref(false)

async function copy() {
  try {
    await navigator.clipboard.writeText(PITCH)
    copied.value = true
    setTimeout(() => (copied.value = false), 2500)
  } catch {
    // clipboard недоступен (file://, старый браузер) — дадим выделить вручную
    window.prompt('Скопируйте текст отклика:', PITCH)
  }
}
</script>

<template>
  <div>
    <div class="section">
      <h2>Контакты</h2>
      <p class="hint">Те же, что в моих резюме на GitHub (cv-zhuk, cv-winwox, cv-saber) — ничего лишнего:</p>
      <p>
        GitHub:
        <a :href="data.candidate.contacts.github" target="_blank" rel="noopener">github.com/Kerarty</a>
        · Telegram:
        <a :href="data.candidate.contacts.telegram" target="_blank" rel="noopener">t.me/Kerarty</a>
        · Email:
        <a :href="'mailto:' + data.candidate.contacts.email">{{ data.candidate.contacts.email }}</a>
      </p>
      <p class="hint">
        Запись на собеседование у компании — через Telegram-бот:
        <a href="https://t.me/recruit_markformelle_bot" target="_blank" rel="noopener">t.me/recruit_markformelle_bot</a>
      </p>
    </div>

    <div class="section">
      <h2>Готовый абзац для отклика</h2>
      <p>{{ PITCH }}</p>
      <button class="btn" @click="copy">{{ copied ? 'Скопировано ✓' : 'Скопировать текст' }}</button>
    </div>
  </div>
</template>
