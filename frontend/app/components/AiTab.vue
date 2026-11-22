<script setup lang="ts">
const REPO = 'https://github.com/Kerarty/cv-mark-formelle'
</script>

<template>
  <div>
    <div class="section">
      <h2>Производственный конвейер</h2>
      <p>
        Вакансия требует ежедневной работы с AI-ассистентами — «умение ставить задачу и критически
        проверять результат». Поэтому досье собрано открытым конвейером, который видно в репозитории:
      </p>

      <div class="conveyor" aria-hidden="true">
        <div class="conveyor-line"><span class="conveyor-dot"></span></div>
      </div>

      <div class="pipe-steps">
        <div class="pipe-step">
          <span class="num">01</span>
          <p class="title">Правила — до кода</p>
          <p>
            <a :href="REPO + '/blob/main/AGENTS.md'" target="_blank" rel="noopener">AGENTS.md</a>
            фиксирует канон: страница живёт без бэкенда, HR нельзя проиграть, факты проверяемы.
            Ассистент не может их нарушить, ревью идёт по ним же.
          </p>
        </div>
        <div class="pipe-step">
          <span class="num">02</span>
          <p class="title">Постановка задачи = контракт</p>
          <p>
            Каждой фазе — тесты HTTP-слоя до реализации (TDD): «SQL-демо возвращает медленный и
            быстрый прогоны, у медленного в плане SCAN, у быстрого INDEX, ускорение ≥ 2×». Задача
            считается выполненной только зелёными тестами.
          </p>
        </div>
        <div class="pipe-step">
          <span class="num">03</span>
          <p class="title">Критическая проверка</p>
          <p>
            Числа прогона SQL-демо измерены на реальном бэкенде (×8.6 и ×28.5 — см.
            <a href="#sql">sql</a>), даты репозиториев — из api.github.com; первый черновик
            SQL-роутера содержал лишний импорт — найден линтером и удалён. Ruff + pytest в CI не
            пропускают «похоже на правду».
          </p>
        </div>
        <div class="pipe-step">
          <span class="num">04</span>
          <p class="title">Субагенты вместо монолога</p>
          <p>
            Дизайн, бэкенд и фронтенд собирались раздельными проходами со своими проверками — так
            же, как в предыдущих 20+ проектах серии cv-* (см. <a href="#fit">fit</a>).
          </p>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="proof">
        <h3>Что это доказывает</h3>
        <p style="margin-bottom: 0">
          Не «пользовался Copilot», а воспроизводимый процесс: правила → контракты-тесты → проверка
          фактами → ревью. Именно его отдел ИИ просит под внедрение ассистентов в бизнес-процессы.
        </p>
      </div>
    </div>
  </div>
</template>
