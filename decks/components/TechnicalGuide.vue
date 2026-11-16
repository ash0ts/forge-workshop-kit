<script setup lang="ts">
import { computed } from 'vue'

type Frame = { id: string; label: string; src: string; caption?: string }
const props = defineProps<{ frames: Frame[]; step: number }>()
const selected = computed(() => Math.max(0, Math.min(Math.floor(props.step || 0), props.frames.length - 1)))
const frame = computed(() => props.frames[selected.value])
</script>

<template>
  <figure class="te-guide-frame" v-if="frame" :data-frame-id="frame.id" :data-frame-index="selected" :data-frame-count="frames.length">
    <img :src="frame.src" :alt="frame.label + (frame.caption ? ': ' + frame.caption : '')" />
    <figcaption aria-live="polite">
      <span>{{ selected + 1 }} / {{ frames.length }}</span>
      <span>{{ frame.label }}</span>
      <span class="te-guide-keys">← Back · Next →</span>
    </figcaption>
  </figure>
</template>

<style scoped>
.te-guide-frame{height:100%;width:100%;margin:0;display:grid;grid-template-rows:minmax(0,1fr) 24px;gap:6px}
.te-guide-frame img{width:100%;height:100%;object-fit:contain;display:block;min-height:0}
.te-guide-frame figcaption{display:flex;gap:16px;align-items:center;margin:0;padding:0 24px;font:13px 'IBM Plex Mono',monospace;color:var(--muted,#60625d)}
.te-guide-keys{margin-left:auto}
@media print{.te-guide-keys{display:none}}
@media(prefers-reduced-motion:reduce){.te-guide-frame{transition:none;animation:none}}
</style>
