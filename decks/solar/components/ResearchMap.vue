<script setup>
import {useId} from 'vue'
const markerId=useId().replace(/:/g,'')
const props=defineProps({level:{default:0},mode:{default:'research'}})
</script>
<template>
<div class="research-map">
<svg :style="{'--arrow':`url(#${markerId})`}" viewBox="0 0 1120 380" role="img" aria-label="Research program with fixed data and scoring, editable model and training code, versioned experiment records, and a fixed-model research agent">
<defs><marker :id="markerId" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#638382"/></marker></defs>
<rect x="255" y="40" width="610" height="290" rx="12" fill="#f0ecdf" stroke="#899e97" stroke-dasharray="7 6"/>
<text x="280" y="71" class="label">RESEARCH PROGRAM</text>
<g><rect x="30" y="142" width="180" height="80" rx="8" fill="#dbe6e1"/><text x="120" y="175" text-anchor="middle">Observations</text><text x="120" y="201" text-anchor="middle" class="small">fixed dates + targets</text><path d="M210 182H300" class="flow"/></g>
<g><rect x="310" y="140" width="220" height="84" rx="8" fill="#163c43"/><text x="420" y="174" text-anchor="middle" fill="#fff">Forecast model</text><text x="420" y="202" text-anchor="middle" fill="#bbd4cb" class="small">trained weights</text><path d="M530 182H600" class="flow"/></g>
<g><rect x="610" y="140" width="210" height="84" rx="8" fill="#bad8cd"/><text x="715" y="174" text-anchor="middle">Prediction</text><text x="715" y="202" text-anchor="middle" class="small">a number or an image</text></g>
<g v-if="level>=1"><rect x="310" y="255" width="220" height="52" rx="6" fill="#f1ca70"/><text x="420" y="288" text-anchor="middle">Model + training code</text><path d="M420 255V232" class="flow"/></g>
<g v-if="level>=2"><path d="M820 182H884" class="flow"/><rect x="895" y="140" width="200" height="84" rx="8" fill="#dbe6e1"/><text x="995" y="172" text-anchor="middle">Independent score</text><text x="995" y="202" text-anchor="middle" class="small">fixed metric + split</text></g>
<g v-if="level>=3"><path d="M715 224V260" class="flow"/><rect x="610" y="268" width="210" height="40" rx="4" fill="#c6d9e7"/><text x="715" y="295" text-anchor="middle" class="small">Source, settings, outputs</text></g>
<g v-if="level>=4"><rect x="30" y="270" width="180" height="70" rx="8" fill="#f1ca70"/><text x="120" y="299" text-anchor="middle">Research agent</text><text x="120" y="325" text-anchor="middle" class="small">fixed model weights</text><path d="M210 290H300" class="flow"/><text x="258" y="322" text-anchor="middle" class="small">edits code</text></g>
</svg>
</div>
</template>
<style scoped>.research-map svg{width:100%;height:370px}.research-map text{font:22px 'IBM Plex Sans';fill:#163c43}.research-map text[fill]{fill:attr(fill)}.research-map text[fill="#fff"]{fill:#fff}.research-map text[fill="#bbd4cb"]{fill:#bbd4cb}.research-map .small{font-size:16px}.research-map .label{font:14px 'IBM Plex Mono';letter-spacing:1px}.flow{fill:none;stroke:#638382;stroke-width:2.5;marker-end:var(--arrow)}</style>
