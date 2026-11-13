<script setup>
import {useId} from 'vue'
const markerId=useId().replace(/:/g,'')
defineProps({level:{default:0},mode:{default:'research'}})
</script>
<template><div class="research-map"><svg :style="{'--arrow':`url(#${markerId})`}" viewBox="0 0 1120 390" role="img" aria-label="Observed inputs enter the forecast model. Its prediction and the separately held future target enter the fixed scorer. The complete execution records source, settings, model weights, predictions and metrics.">
<defs><marker :id="markerId" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6" fill="none" stroke="#52776d" stroke-width="1.7"/></marker></defs>
<g><text x="25" y="62">Input window</text><text x="25" y="96" class="small">Observed history only</text><path d="M25 178L43 166L62 171L80 150L100 160L120 140L140 151L158 146L180 158" stroke="#2b7a78" stroke-width="3" fill="none"/><text x="25" y="220" class="small">Schematic measurements</text><path d="M195 160H278" class="flow"/></g>
<g><rect x="295" y="80" width="240" height="164" rx="6" fill="#163c43"/><text x="415" y="119" text-anchor="middle" class="white">Forecast model</text><text x="415" y="158" text-anchor="middle" class="mono white">prediction = model(x)</text><text x="415" y="204" text-anchor="middle" class="small white">Uses learned weights</text><path d="M548 160H608" class="flow"/></g>
<g><text x="630" y="151">Prediction</text><text x="630" y="188" class="small">Future value or image</text></g>
<g v-if="level>=1"><path d="M295 286H535V356H295Z" fill="#f1ca70"/><text x="313" y="315" class="mono">build_model + fit</text><text x="313" y="342" class="small">Save the executed Python</text><path d="M415 282V254" class="flow"/></g>
<g v-if="level>=2"><path d="M810 160H882" class="flow"/><rect x="897" y="106" width="200" height="138" rx="5" fill="#dbe6e1"/><text x="997" y="149" text-anchor="middle">Fixed scorer</text><text x="997" y="187" text-anchor="middle" class="mono">abs(pred − target)</text><text x="997" y="217" text-anchor="middle" class="small">Same dates + metric</text><text x="997" y="33" text-anchor="middle">Observed future</text><path d="M997 47V93" class="flow"/></g>
<g v-if="level>=3"><path d="M560 284H1098V357H560Z" fill="#c6d9e7"/><text x="581" y="314">Record this execution</text><text x="581" y="343" class="small">Code · config · data identity · weights · outputs</text><path d="M760 213V270M997 250V270" class="flow"/></g>
</svg></div></template>
<style scoped>.research-map svg{width:100%;height:390px}.research-map text{font:25px 'IBM Plex Sans';fill:#163c43}.research-map .small{font-size:19px}.research-map .mono{font:18px 'IBM Plex Mono'}.research-map .white{fill:#f6f2e7}.flow{fill:none;stroke:#52776d;stroke-width:2;marker-end:var(--arrow)}</style>
