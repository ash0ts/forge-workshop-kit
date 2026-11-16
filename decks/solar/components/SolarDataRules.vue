<script setup>
import {useId} from 'vue'
defineProps({mode:{default:'gaps'}})
const marker=useId().replace(/:/g,'')
const descriptions={gaps:'Schematic timeline: a complete input and target interval inside a split is accepted. An interval crossing missing observations is rejected. An interval crossing the February 10 to 11 split boundary is rejected even when all readings exist.',adoption:'After training the composed code, compare its fixed validation error with the parent. Strictly lower error adopts the tested source and weights. Equal, worse, failed or missing results retain the parent. Both decisions save a lesson before the next round.', 'zero-head':'Only the last convolution layer weights and bias are initialized to zero. Earlier layers retain normal initialization. The output correction is initially zero, so the residual forecast equals the current image before training.'}
</script>
<template><svg viewBox="0 0 1120 390" role="img" :aria-label="descriptions[mode]" :style="{'--arrow':`url(#${marker})`}"><defs><marker :id="marker" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6" fill="none" stroke="#52776d" stroke-width="1.7"/></marker></defs>
<g v-if="mode==='gaps'">
 <text x="25" y="27" class="label">SCHEMATIC WINDOWS · POSITIONS DO NOT REPRESENT OBSERVED FLUX</text>
 <g v-for="(label,i) in ['Complete interval','Missing observations','Crosses date split']" :key="label" :transform="`translate(0 ${70+i*102})`"><text x="25" y="24">{{label}}</text><path d="M300 18H960" class="line"/><rect x="320" y="0" width="330" height="36" fill="#bad8cd"/><path d="M650 18H850" class="line" stroke-dasharray="4 5"/><circle cx="860" cy="18" r="10" fill="#f1ca70"/><text v-if="i===0" x="315" y="68" class="small">Input history</text><text v-if="i===0" x="795" y="68" class="small">Future target</text><text x="990" y="24">{{i===0?'Keep':'Skip'}}</text><g v-if="i===1"><rect x="710" y="-12" width="50" height="65" fill="#f6f2e7"/><path d="M715 -8L755 40M755 -8L715 40" stroke="#b57339" stroke-width="3"/><text x="690" y="72" class="small">A gap anywhere in the interval rejects it.</text></g><g v-if="i===2"><line x1="710" y1="-23" x2="710" y2="59" stroke="#b57339" stroke-width="3"/><text x="630" y="76" class="small">Feb 10</text><text x="740" y="76" class="small">Feb 11</text></g></g>
</g>
<g v-else-if="mode==='adoption'">
 <text x="25" y="33" class="label">FIXED VALIDATION SCORE · FINAL-TEST RESULTS ARE NOT READ</text>
 <text x="35" y="108">Parent error</text><text x="35" y="154">Composed version’s error</text><path d="M330 126H410" class="arrow"/>
 <path d="M570 60L715 135L570 210L425 135Z" fill="#f1ca70"/><text x="570" y="124" text-anchor="middle">Is the new error</text><text x="570" y="155" text-anchor="middle">strictly lower?</text>
 <path d="M715 135H760V86H825" class="arrow"/><text x="765" y="62" class="small">Yes</text><text x="850" y="83">Adopt tested version</text><text x="850" y="117" class="small">Source + trained weights</text>
 <path d="M570 210V285H825" class="arrow"/><text x="594" y="265" class="small">No, or no valid result</text><text x="850" y="291">Retain the parent</text>
 <text x="35" y="355">Save the decision and lesson, then use the retained code in round two.</text>
</g>
<g v-else-if="mode==='zero-head'">
 <text x="25" y="28" class="label">RECORDED EDIT · ONLY THE FINAL CONV2D CHANGES INITIALIZATION</text>
 <text x="25" y="98">Two input images</text><path d="M218 91H273" class="arrow"/>
 <g v-for="i in 3" :key="i"><rect :x="292+(i-1)*13" :y="60+(i-1)*12" width="105" height="80" fill="#bad8cd" stroke="#52776d"/></g><text x="365" y="196" text-anchor="middle">Earlier layers</text><text x="365" y="227" text-anchor="middle" class="small">Normal initialization</text>
 <path d="M440 100H520" class="arrow"/><rect x="542" y="58" width="170" height="100" fill="#f1ca70"/><text x="627" y="95" text-anchor="middle" class="mono">self.net[-1]</text><text x="627" y="130" text-anchor="middle" class="mono">W = 0, b = 0</text><text x="627" y="196" text-anchor="middle">Output layer</text>
 <path d="M730 100H812" class="arrow"/><text x="835" y="107">Correction = 0</text>
 <text x="25" y="305" class="mono">forecast = current_image + 0</text><text x="25" y="350">Before training, this returns persistence. Training then updates the weights.</text>
</g>
</svg></template><style scoped>svg{display:block;width:100%;height:390px;margin-top:12px}text{font:23px 'IBM Plex Sans',Arial;fill:#163c43}.small{font-size:19px}.mono{font:20px 'IBM Plex Mono',monospace}.label{font:16px 'IBM Plex Mono',monospace;letter-spacing:1px;fill:#52776d}.arrow,.line{fill:none;stroke:#52776d;stroke-width:2}.arrow{marker-end:var(--arrow)}</style>
