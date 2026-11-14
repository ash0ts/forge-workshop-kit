<script setup>
defineProps({level:{default:1}})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 420" role="img" aria-label="Within a ticket, tool observations are appended to the model's history. Between improvement rounds, the selected harness and an evidence-linked lesson persist. Each new execution resets the office state. Language-model weights and tested Python tools stay fixed.">
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="26" style="font-size:21px">Within one customer ticket</text>
<rect x="20" y="48" width="1080" height="117" rx="8" fill="#e4eadd"/>
<text x="42" y="89" style="font-size:23px">Request → action → tool result → next request</text>
<text x="42" y="132" style="font-size:21px">The result extends the conversation. It does not train the model.</text>
<g v-if="level>=2">
<text x="20" y="211" style="font-size:21px">Between improvement rounds</text>
<rect x="20" y="233" width="515" height="122" rx="8" fill="#d9e6ef"/>
<text x="42" y="273" style="font-size:23px">Carry forward</text>
<text x="42" y="313" style="font-size:21px">Selected harness + lesson + supporting run</text>
<rect x="561" y="233" width="539" height="122" rx="8" fill="#f3e4b7"/>
<text x="581" y="273" style="font-size:23px">Start the new case again</text>
<text x="581" y="313" style="font-size:21px">Fresh account state + the new customer ticket</text>
</g>
<text x="20" y="404" style="font-size:19px">Fixed throughout the comparison: language-model weights, tested Python tools, cases, and final grading.</text>
</g></svg>
</template>
