<script setup>
import data from '../data/recorded-final.json'
const props=defineProps({recorded:Boolean})
const cases=['already-refunded','two-invoices','onboarding-recovery','clarify-access']
const labels=['Already refunded','Two different invoices','Onboarding recovery','Missing access details']
const versions=['Starting instructions','Manual revision','Agent-selected']
const versionLabels=['Starting','Manual','Agent-selected']
const colors=['#e2e5df','#d9e6ef','#edcdaa']
function row(c,v){return data.executions.find(r=>r.Case===c && r.Version.startsWith(v))}
function total(v){return data.executions.filter(r=>r.Version.startsWith(v)).reduce((n,r)=>n+r['Tool calls'],0)}
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 430" role="img" :aria-label="recorded?'Recorded rehearsal: starting, manual and agent-selected harnesses all passed account and grounded-explanation checks on the same four cases. Tool-call totals were 12, 13, and 13. Each result links to its conversation.':'Planned comparison: four distinct fresh cases are rows and starting, manual, and agent-selected harnesses are columns. Each cell is one isolated execution with state and explanation scores, for twelve executions total.'">
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="32" style="font-size:19px">SAME FRESH CASE</text>
<g v-for="(v,j) in versions" :key="v"><rect :x="330+j*260" y="9" width="245" height="47" rx="7" :fill="colors[j]"/><text :x="452+j*260" y="40" text-anchor="middle" style="font-size:24px">{{versionLabels[j]}}</text></g>
<g v-for="(c,i) in cases" :key="c">
<text x="20" :y="109+i*70" style="font-size:23px">{{labels[i]}}</text><text x="20" :y="133+i*70" style="font-size:16px">{{c}}</text>
<g v-for="(v,j) in versions" :key="v">
<rect :x="330+j*260" :y="72+i*70" width="245" height="61" rx="7" :fill="colors[j]"/>
<a v-if="recorded" :href="row(c,v)?.Conversation" target="_blank" tabindex="0" :aria-label="`${labels[i]}, ${versionLabels[j]}: open recorded execution`">
<text :x="349+j*260" :y="98+i*70" style="font-size:21px">Account: {{row(c,v)?.['Correct account']===true?'pass':row(c,v)?.['Correct account']===false?'fail':'unavailable'}}</text>
<text :x="349+j*260" :y="123+i*70" style="font-size:19px">Grounded: {{row(c,v)?.['Grounded explanation']===true?'pass':row(c,v)?.['Grounded explanation']===false?'fail':'unavailable'}} ↗</text>
</a>
<text v-else :x="452+j*260" :y="110+i*70" text-anchor="middle" style="font-size:22px">1 execution</text>
</g></g>
<g v-if="recorded"><text x="20" y="390" style="font-size:22px">Total tool calls</text><text v-for="(v,j) in versions" :key="v" :x="452+j*260" y="390" text-anchor="middle" style="font-size:25px">{{total(v)}}</text></g>
<text v-else x="20" y="390" style="font-size:22px">Reset each case for each harness. Score account state and explanation separately.</text>
<text x="20" y="423" style="font-size:17px">{{recorded?'One recorded rehearsal; four distinct tasks. No measured pass-rate gain. Click a cell to inspect its actual conversation.':'Four cases × three harnesses = twelve executions. These are four tasks, not twelve independent tasks.'}}</text>
</g></svg>
</template>
