<script setup lang="ts">
/** Код-блок с минимальной подсветкой SQL: строки, комментарии, ключевые слова. */

const props = defineProps<{ code: string }>()

const KEYWORDS =
  /\b(SELECT|FROM|WHERE|JOIN|ON|AND|OR|BETWEEN|GROUP BY|ORDER BY|LIMIT|DESC|ASC|COUNT|SUM|AS|CREATE|INDEX|SET|TRANSACTION|ISOLATION|LEVEL|BEGIN|COMMIT|ROLLBACK|UPDATE|INSERT|INTO|VALUES|TRY|CATCH|IF|THROW|WITH|NOT|NULL)\b/g

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function highlightLine(line: string): string {
  const cut = line.indexOf('--')
  const code = cut >= 0 ? line.slice(0, cut) : line
  const comment = cut >= 0 ? line.slice(cut) : ''
  let h = esc(code)
  h = h.replace(/'([^']*)'/g, `<span class="tk-s">'$1'</span>`)
  h = h.replace(KEYWORDS, `<span class="tk-k">$1</span>`)
  return h + (comment ? `<span class="tk-c">${esc(comment)}</span>` : '')
}

const html = computed(() => props.code.split('\n').map(highlightLine).join('\n'))
</script>

<template>
  <pre class="code"><code v-html="html" /></pre>
</template>
