<script setup>
const props = defineProps({stage: {type: Number, default: 0}})
</script>
<template>
<svg class="factory-map" viewBox="0 0 1120 350" role="img" aria-label="An approved transit feature becomes tasks. Two workers edit isolated copies. An integration step tests their combined code. A checked lesson can guide a later task.">
<defs><marker id="factory-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#61746e"/></marker></defs>
<g><rect x="0" y="112" width="195" height="105" rx="7" fill="#dfe3e0"/><text x="20" y="147" class="major">Feature contract</text><text x="20" y="181" class="minor">Inputs + checks</text></g>
<g v-if="stage>=1"><path d="M195 163H245" class="wire"/><rect x="245" y="112" width="180" height="105" rx="7" fill="#e7e8d5"/><text x="265" y="147" class="major">Task board</text><text x="265" y="181" class="minor">Ready work + owners</text></g>
<g v-if="stage>=2"><path d="M425 155C455 155 450 75 495 75M425 175C455 175 450 265 495 265" class="wire"/><rect x="495" y="25" width="245" height="100" rx="7" fill="#d6e7ee"/><text x="515" y="61" class="major">Worker A</text><text x="515" y="94" class="minor">Own files + own context</text><rect x="495" y="215" width="245" height="100" rx="7" fill="#f0dfce"/><text x="515" y="251" class="major">Worker B</text><text x="515" y="284" class="minor">Own files + own context</text></g>
<g v-if="stage>=3"><path d="M740 75C780 75 770 147 815 147M740 265C780 265 770 185 815 185" class="wire"/><rect x="815" y="112" width="295" height="105" rx="7" fill="#d5e5d8"/><text x="835" y="147" class="major">Review and integrate</text><text x="835" y="181" class="minor">Combined app + tests</text></g>
<g v-if="stage>=4"><rect x="780" y="260" width="330" height="65" rx="7" fill="#f4edda" stroke="#a2b1a1"/><text x="798" y="300" class="minor">Checked lesson → later worker</text><path d="M960 217V256" class="evidence"/><text x="776" y="29" class="minor">Dashed line: evidence reviewed</text></g>
</svg>
</template>
<style scoped>
.factory-map{width:100%;height:350px;margin-top:12px}.major{font:600 23px 'IBM Plex Sans';fill:#163c43}.minor{font:18px 'IBM Plex Sans';fill:#365d55}.wire{stroke:#61746e;stroke-width:2.5;fill:none;marker-end:url(#factory-arrow)}.evidence{stroke:#61746e;stroke-width:2;stroke-dasharray:7 5;fill:none;marker-end:url(#factory-arrow)}
</style>
