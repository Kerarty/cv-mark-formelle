export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  app: {
    // GitHub Pages — project site: /cv-mark-formelle/; локально и в docker — /
    baseURL: process.env.NUXT_APP_BASE_URL || '/',
    head: {
      htmlAttrs: { lang: 'ru' },
      title: 'cv-mark-formelle — досье кандидата как микросервис',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Интерактивное резюме для Марк Формэль: FastAPI + Nuxt, SQL-демо на 200k строк, честный маппинг требований.',
        },
      ],
    },
  },
  runtimeConfig: {
    public: {
      // LIVE-режим: где живёт реальный FastAPI (docker-compose up → 127.0.0.1:8000)
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000',
    },
  },
})
