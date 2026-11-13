<script setup>
const sequence=['get_account','refund_payment','get_account']
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 415" role="img" aria-label="Recorded first-round probe comparison. Both candidates read the account, refund the duplicate, and read the account again. Candidate A finishes in four tool calls. Candidate B's first finish is rejected, then it calls check_work and finishes, taking six tool calls. Both account checks pass. This is a development probe, not the final evaluation.">
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="30" style="font-size:20px">RECORDED BILLING PROBES · SAME INITIAL ACCOUNT</text>
<text x="20" y="94" style="font-size:25px">Shared first three calls</text>
<g v-for="(name,i) in sequence" :key="i"><rect :x="20+i*300" y="115" width="270" height="65" rx="8" fill="#dce8df"/><text :x="155+i*300" y="155" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:23px">{{name}}</text><text v-if="i<2" :x="295+i*300" y="154" style="font-size:25px">→</text></g>
<text x="20" y="238" style="font-size:23px">A · Retain parent</text><rect x="310" y="209" width="215" height="60" rx="8" fill="#d9e6ef"/><text x="417" y="247" text-anchor="middle" style="font-size:22px">finish accepted</text><text x="890" y="239" style="font-size:23px">4 calls · account pass</text>
<text x="20" y="326" style="font-size:23px">B · Completion gate</text><rect x="310" y="295" width="215" height="60" rx="8" fill="#edcdaa"/><text x="417" y="333" text-anchor="middle" style="font-size:22px">finish rejected</text><text x="532" y="333" style="font-size:25px">→</text><rect x="563" y="295" width="150" height="60" rx="8" fill="#edcdaa"/><text x="638" y="333" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:20px">check_work</text><text x="721" y="333" style="font-size:25px">→</text><rect x="751" y="295" width="124" height="60" rx="8" fill="#edcdaa"/><text x="813" y="333" text-anchor="middle" style="font-size:21px">finish</text><text x="890" y="326" style="font-size:23px">6 calls · account pass</text>
<text x="22" y="406" style="font-size:18px">The gate changed the tool sequence without improving this probe’s account outcome. These are development executions.</text>
</g></svg>
</template>
