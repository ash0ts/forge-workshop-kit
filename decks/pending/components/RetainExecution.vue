<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 415" role="img" aria-label="Recorded first-round KEEP: the parent harness and composition have the same fingerprint 5cfd358201e0. The controller still creates a new composition-test execution from the case's original state. The decision and execution are new records, while the harness files remain unchanged.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="27" style="font-size:20px">RECORDED BILLING ROUND</text>
<rect x="20" y="58" width="280" height="150" rx="10" fill="#dce8df"/><text x="40" y="94" style="font-size:24px">Parent harness</text><text x="40" y="132" style="font-size:21px">current instructions + skill</text><text x="40" y="178" font-family="IBM Plex Mono" style="font-size:22px">5cfd358201e0</text>
<path d="M308 132H399" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="407" y="58" width="300" height="150" rx="10" fill="#f1ca70"/><text x="427" y="94" style="font-size:24px">Composition decision</text><text x="427" y="132" style="font-size:22px">Retain this version</text><text x="427" y="178" font-family="IBM Plex Mono" style="font-size:22px">5cfd358201e0</text>
<path d="M714 132H805" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="813" y="58" width="287" height="150" rx="10" fill="#d9e6ef"/><text x="833" y="94" style="font-size:24px">Confirming execution</text><text x="833" y="132" style="font-size:21px">run the same files again</text><text x="833" y="178" style="font-size:21px">case reset to initial state</text>
<path d="M40 236H688" stroke="#527b72" stroke-width="2"/><text x="357" y="269" text-anchor="middle" style="font-size:23px">Same executable content</text>
<path d="M427 298H1080" stroke="#b6783d" stroke-width="2"/><text x="754" y="333" text-anchor="middle" style="font-size:23px">New decision and execution records</text>
<text x="20" y="395" style="font-size:19px">The controller tests every composition, including KEEP. The new run can differ because model execution is nondeterministic.</text>
</g></svg>
</template>
