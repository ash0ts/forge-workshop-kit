<script setup>
import {useId} from 'vue'
defineProps({level:{default:1}})
const marker=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 410" role="img" aria-label="The Python loop constructs a request from instructions, office rules, a tool guide, available skill names, and the ticket. The fixed model returns an action. Python dispatches it to a tool, changes the simulated office state, and appends the result. A saved skill's contents enter only after read_skill.">
<defs><marker :id="marker" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="18" y="25" style="font-size:20px">Request built by Python</text>
<rect x="18" y="42" width="425" height="240" rx="7" fill="#e4eadd"/>
<text x="36" y="77" style="font-size:22px">System instructions + office rules</text>
<text x="36" y="118" style="font-size:22px">Tool guide: names and arguments</text>
<text x="36" y="159" style="font-size:22px">Available skill names</text>
<text x="36" y="203" style="font-size:22px">Customer ticket</text>
<text x="36" y="250" style="font-size:19px">Later requests also contain action history.</text>
<path d="M455 150H500" stroke="#527b72" stroke-width="3" :marker-end="`url(#${marker})`"/>
<rect x="513" y="93" width="222" height="126" rx="7" fill="#163c43"/>
<text x="624" y="135" text-anchor="middle" style="font-size:24px" fill="#fff">Language model</text>
<text x="624" y="176" text-anchor="middle" style="font-size:20px" fill="#dce8df">Weights stay fixed</text>
<g v-if="level>=2">
<path d="M747 150H790" stroke="#527b72" stroke-width="3" :marker-end="`url(#${marker})`"/>
<rect x="804" y="80" width="298" height="170" rx="7" fill="#d9e6ef"/>
<text x="823" y="116" style="font-size:22px">Python receives an action</text>
<text x="823" y="157" style="font-size:21px">Dispatch → tool function</text>
<text x="823" y="198" style="font-size:21px">Read or update office state</text>
<text x="823" y="232" style="font-size:18px">JSON alone does not run a tool.</text>
<path d="M953 261V310H235V290" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${marker})`"/>
<text x="480" y="345" style="font-size:21px">Append the action and actual tool result</text>
</g>
<text v-if="level===1" x="18" y="350" style="font-size:22px">A skill name is available here. Its file contents are not loaded yet.</text>
<text x="18" y="395" style="font-size:18px">Source: pending/harness.py build_messages and pending/loop.py run_employee. Simplified layout; actual fields are shown in code.</text>
</g></svg>
</template>
