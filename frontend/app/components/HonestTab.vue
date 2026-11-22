<script setup lang="ts">
const REPO = 'https://github.com/Kerarty/cv-mark-formelle'
</script>

<template>
  <div>
    <div class="section">
      <h2>Отдел техконтроля: чего пока нет</h2>
      <ul class="log">
        <li>
          <div class="title">Коммерческого опыта разработки</div>
          <p class="muted" style="margin: 4px 0 0">
            Python — университетский курс плюс самостоятельное углубление; код в боевых
            репозиториях — учебные и конкурсные задания, playable-проекты.
          </p>
        </li>
        <li>
          <div class="title">MS SQL Server в бою</div>
          <p class="muted" style="margin: 4px 0 0">
            Индексы, JOIN и изоляция — теория, доведённая до интерактива в этом проекте на SQLite;
            боевых планов выполнения MS SQL не видел.
          </p>
        </li>
        <li>
          <div class="title">FastAPI / Nuxt до этого проекта</div>
          <p class="muted" style="margin: 4px 0 0">
            Стек собран в этом резюме с нуля за спринт — роутинг, Pydantic v2, тесты, docker-compose,
            CI. Это не замена продакшену, но рабочий уровень входа.
          </p>
        </li>
      </ul>
    </div>

    <div class="section">
      <div class="proof">
        <h3>Что есть вместо</h3>
        <p style="margin-bottom: 0">
          Проверяемые артефакты: 35 репозиториев, 23 резюме-проекта за ~7 недель, SDK playable-рекламы,
          Unity-головоломка на 8 уровней. Навык, который просит вакансия, — ежедневная работа с
          ассистентами с критической проверкой — показан на этом же досье: правила в
          <a :href="REPO + '/blob/main/AGENTS.md'" target="_blank" rel="noopener">AGENTS.md</a>, тесты в
          <a :href="REPO + '/tree/main/backend/tests'" target="_blank" rel="noopener">backend/tests</a>,
          CI зелёный на каждом коммите.
        </p>
      </div>
    </div>
  </div>
</template>
