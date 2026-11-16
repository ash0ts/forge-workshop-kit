<script setup lang="ts">
import SharedTechnicalGuide from "../../components/TechnicalGuide.vue"

defineProps<{
  frames: { id: string; label: string; src: string; caption?: string }[]
  step: number
}>()
</script>

<template>
  <SharedTechnicalGuide :frames="frames" :step="step" />
</template>
