<script setup lang="ts">
import type { FitStatus } from '~/types'

const props = defineProps<{ status: FitStatus }>()

const LABEL: Record<FitStatus, string> = {
  full: '✓ есть',
  partial: '◐ частично',
  plan: '○ план',
}
</script>

<template>
  <span class="badge" :class="props.status">{{ LABEL[props.status] }}</span>
</template>
