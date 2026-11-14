<script setup>
defineProps({stage:{type:Number,default:0}})
</script>
<template>
<svg class="contract-map" viewBox="0 0 1120 330" role="img" aria-label="The departures board joins stops, trips and service dates. The query module and display module share an agreed interface; integration waits for both.">
<defs><marker id="contract-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#61746e"/></marker></defs>
<rect x="0" y="18" width="275" height="130" rx="7" fill="#d6e7ee"/><text x="22" y="57" class="major">Query departures</text><text x="22" y="95" class="minor">Stop + time → records</text><text x="22" y="126" class="minor">Owns query.py</text>
<rect x="0" y="184" width="275" height="130" rx="7" fill="#f0dfce"/><text x="22" y="223" class="major">Render the board</text><text x="22" y="261" class="minor">Records → readable board</text><text x="22" y="292" class="minor">Owns presentation.py</text>
<g v-if="stage>=1"><path d="M275 83C330 83 325 143 380 143M275 249C330 249 325 190 380 190" class="wire"/><rect x="380" y="107" width="330" height="120" rx="7" fill="#e7e8d5"/><text x="404" y="148" class="major">Integrate the modules</text><text x="404" y="186" class="minor">Wait for both reviewed patches</text></g>
<g v-if="stage>=2"><path d="M710 167H765" class="wire"/><rect x="765" y="107" width="345" height="120" rx="7" fill="#d5e5d8"/><text x="785" y="148" class="major">Check the displayed result</text><text x="785" y="186" class="minor">Right stop, service day and order</text></g>
</svg>
</template>
<style scoped>
.contract-map{width:100%;height:330px}.major{font:600 23px 'IBM Plex Sans';fill:#163c43}.minor{font:18px 'IBM Plex Sans';fill:#365d55}.wire{stroke:#61746e;stroke-width:2.5;fill:none;marker-end:url(#contract-arrow)}
</style>
