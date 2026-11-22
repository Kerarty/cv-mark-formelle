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
      <h2>Этикетка изделия</h2>
      <div class="labelcard">
        <p class="tag-handle">{{ data.candidate.handle }}</p>
        <p class="hint" style="margin: 0 0 6px">
          Те же контакты, что в резюме на GitHub (cv-zhuk, cv-winwox, cv-saber) — ничего лишнего.
        </p>
        <Barcode />
        <div class="contactlinks">
          <a :href="data.candidate.contacts.github" target="_blank" rel="noopener"><b>github</b>github.com/Kerarty</a>
          <a :href="data.candidate.contacts.telegram" target="_blank" rel="noopener"><b>telegram</b>t.me/Kerarty</a>
          <a :href="'mailto:' + data.candidate.contacts.email"><b>email</b>{{ data.candidate.contacts.email }}</a>
        </div>
        <p class="hint" style="margin-bottom: 0">
          Запись на собеседование у компании — через Telegram-бот:
          <a href="https://t.me/recruit_markformelle_bot" target="_blank" rel="noopener">t.me/recruit_markformelle_bot</a>
        </p>
      </div>
    </div>

    <div class="section">
      <h2>Готовый абзац для отклика</h2>
      <div class="pitch">
        <p>{{ PITCH }}</p>
        <button class="btn" @click="copy">{{ copied ? 'скопировано ✓' : 'скопировать текст' }}</button>
      </div>
    </div>
  </div>
</template>
