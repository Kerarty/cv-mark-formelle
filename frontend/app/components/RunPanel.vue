<script setup lang="ts">
import type { RunResult } from '~/types'

const props = defineProps<{ result: RunResult | null }>()

const maxMs = computed(() => (props.result ? Math.max(props.result.slow.elapsed_ms, props.result.fast.elapsed_ms) : 1))

function width(ms: number): string {
  return `${Math.max((ms / maxMs.value) * 100, 2)}%`
}
</script>

<template>
  <div v-if="props.result" style="margin-top: 16px">
    <span class="speedup">×{{ props.result.speedup }} <small>быстрее с индексом</small></span>
    <div class="bar-row">
      <span class="bar-label">без индекса</span>
      <div class="bar"><i class="slow" :style="{ '--w': width(props.result.slow.elapsed_ms) }" /></div>
      <span class="bar-ms">{{ props.result.slow.elapsed_ms }} ms</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">с индексом</span>
      <div class="bar"><i class="fast" :style="{ '--w': width(props.result.fast.elapsed_ms) }" /></div>
      <span class="bar-ms">{{ props.result.fast.elapsed_ms }} ms</span>
    </div>

    <h3>План без индекса</h3>
    <pre class="planbox">{{ props.result.slow.plan }}</pre>
    <h3>План с индексом</h3>
    <pre class="planbox">{{ props.result.fast.plan }}</pre>

    <h3>Строки (первые 10)</h3>
    <div class="tscroll">
      <table>
        <thead>
          <tr>
            <th v-for="c in props.result.columns" :key="c">{{ c }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in props.result.rows.slice(0, 10)" :key="i">
            <td v-for="(cell, j) in row" :key="j" :class="{ num: typeof cell === 'number' }">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
