<script setup lang="ts">
const props = defineProps<{ value: unknown }>()

const text = computed(() => JSON.stringify(props.value, null, 2))
</script>

<template>
  <pre class="planbox">{{ text }}</pre>
</template>
