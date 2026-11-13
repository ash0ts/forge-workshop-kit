<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 425" role="img" aria-label="Two evaluations read different parts of a completed execution. The deterministic scorer compares whole final accounts against expected accounts and checks required resolution. The explanation judge receives the mission, recorded events, and final reply, and returns grounded and complete booleans with a reason. Its response validator checks types, not truth.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="30" y="29" style="font-size:24px">Account correctness</text><text x="615" y="29" style="font-size:24px">Explanation accuracy</text>
<rect x="20" y="45" width="495" height="108" rx="9" fill="#dce8df"/><text x="40" y="79" style="font-size:22px">Actual accounts + final resolution</text><text x="40" y="113" style="font-size:21px">Expected accounts + required resolution</text><text x="40" y="141" style="font-size:18px">constructed from the case’s initial state and objective</text>
<rect x="600" y="45" width="500" height="108" rx="9" fill="#d9e6ef"/><text x="620" y="79" style="font-size:22px">Customer mission + recorded tool events</text><text x="620" y="113" style="font-size:21px">Agent’s final explanation + judge rubric</text><text x="620" y="141" style="font-size:18px">the judge does not receive the expected accounts</text>
<path d="M267 159V194" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><path d="M850 159V194" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="20" y="202" width="495" height="91" rx="9" fill="#dce8df"/><text x="40" y="236" font-family="IBM Plex Mono" style="font-size:22px">grade(case, run)</text><text x="40" y="269" style="font-size:21px">Compare account state and completion.</text>
<rect x="600" y="202" width="500" height="91" rx="9" fill="#d9e6ef"/><text x="620" y="236" font-family="IBM Plex Mono" style="font-size:22px">judge_explanation(…, rubric)</text><text x="620" y="269" style="font-size:21px">Ask a model whether the reply is supported.</text>
<path d="M267 299V330" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><path d="M850 299V330" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<text x="40" y="365" font-family="IBM Plex Mono" style="font-size:21px">state_correct · completion_correct</text><text x="620" y="365" font-family="IBM Plex Mono" style="font-size:21px">grounded · complete · reason</text>
<text x="22" y="412" style="font-size:18px">my_judge_validation checks the response fields and types. Read the reason to assess whether the judgment is supported.</text>
</g></svg>
</template>
