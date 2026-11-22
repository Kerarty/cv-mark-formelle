<script setup lang="ts">
/** Декоративный штрих-код бирки: детерминированные полосы, aria-hidden, не сканер. */

const PATTERN = [
  3, 1, 1, 2, 1, 4, 1, 1, 3, 2, 1, 1, 2, 3, 1, 1, 4, 1, 2, 1, 1, 3, 1, 2, 2, 1, 3, 1, 1, 1, 4, 2, 1, 3, 1, 1, 2, 1,
]

const rects: { x: number; w: number }[] = []
let x = 0
PATTERN.forEach((w, i) => {
  if (i % 2 === 0) rects.push({ x, w })
  x += w
})
const total = x
</script>

<template>
  <svg
    class="tag-code"
    :viewBox="`0 0 ${total} 40`"
    preserveAspectRatio="none"
    aria-hidden="true"
    fill="currentColor"
  >
    <rect v-for="(r, i) in rects" :key="i" :x="r.x" y="0" :width="r.w" height="40" />
  </svg>
</template>
