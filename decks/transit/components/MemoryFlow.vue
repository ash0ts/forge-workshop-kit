<script setup>
defineProps({stage:{type:Number,default:0}})
</script>
<template>
<svg class="memory-map" viewBox="0 0 1120 325" role="img" aria-label="A failed integration check supports a proposed lesson. A person verifies its scope and evidence. A later worker retrieves the approved lesson and tests the next feature.">
<defs><marker id="memory-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#61746e"/></marker></defs>
<g><rect x="5" y="25" width="250" height="140" rx="7" fill="#dfe3e0"/><text x="23" y="66" class="major">Execution record</text><text x="23" y="105" class="minor">Test, actual output, code</text><text x="23" y="139" class="minor">Preserve the original event</text></g>
<g v-if="stage>=1"><path d="M255 94H300" class="wire"/><rect x="300" y="25" width="250" height="140" rx="7" fill="#f0dfce"/><text x="318" y="66" class="major">Proposed lesson</text><text x="318" y="105" class="minor">Rule + scope + source</text><text x="318" y="139" class="minor">Still a claim to check</text></g>
<g v-if="stage>=2"><path d="M550 94H595" class="wire"/><rect x="595" y="25" width="250" height="140" rx="7" fill="#d5e5d8"/><text x="613" y="66" class="major">Approved memory</text><text x="613" y="105" class="minor">Supported by this test</text><text x="613" y="139" class="minor">Valid for this contract</text></g>
<g v-if="stage>=3"><path d="M720 165V214" class="wire"/><rect x="25" y="220" width="1070" height="80" rx="7" fill="#d6e7ee"/><text x="48" y="269" class="major">Fresh worker → matching memory read → new patch → independent test</text></g>
</svg>
</template>
<style scoped>
.memory-map{width:100%;height:325px;margin-top:15px}.major{font:600 24px 'IBM Plex Sans';fill:#163c43}.minor{font:19px 'IBM Plex Sans';fill:#365d55}.wire{stroke:#61746e;stroke-width:2.5;fill:none;marker-end:url(#memory-arrow)}
</style>
