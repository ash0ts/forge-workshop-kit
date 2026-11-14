<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 420" role="img" aria-label="With verify_before_finish true, finish is accepted only when check_work passed on the current state. A missing, failed or stale check causes a rejected finish. A later write changes the state fingerprint and invalidates the earlier check. check_work is public development feedback, separate from the final independent grade.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="14" width="1080" height="63" rx="9" fill="#f3e4b7"/><text x="40" y="53" font-family="IBM Plex Mono" style="font-size:24px">workflow.json: verify_before_finish = true</text>
<rect x="20" y="122" width="450" height="86" rx="9" fill="#edcdaa"/><text x="40" y="150" style="font-size:24px">No passing check for this state</text><text x="40" y="189" style="font-size:20px">missing check, failed check, or later write</text>
<path d="M478 166H688" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="582" y="147" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:23px">finish</text>
<rect x="698" y="122" width="402" height="86" rx="9" fill="#edcdaa"/><text x="718" y="150" style="font-size:24px">Rejected</text><text x="718" y="180" style="font-size:19px"><tspan x="718">“Check the current work</tspan><tspan x="718" dy="23"> before submitting.”</tspan></text>
<rect x="20" y="246" width="450" height="86" rx="9" fill="#dce8df"/><text x="40" y="280" style="font-size:24px">check_work passed</text><text x="40" y="313" style="font-size:20px">saved state fingerprint still matches world</text>
<path d="M478 289H688" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="582" y="271" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:23px">finish</text>
<rect x="698" y="246" width="402" height="86" rx="9" fill="#dce8df"/><text x="718" y="280" style="font-size:24px">Accepted</text><text x="718" y="313" style="font-size:20px">save the agent’s final explanation</text>
<text x="22" y="386" style="font-size:21px">check_work is public development feedback. Final scoring still checks the expected account and resolution.</text>
<text x="22" y="415" style="font-size:17px">The completion gate controls when the agent can stop. Passing it does not establish that the final independent grade will pass.</text>
</g></svg>
</template>
