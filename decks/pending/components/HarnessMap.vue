<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
defineProps({level:{default:0}})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 425" role="img" aria-label="Harness settings feed a Python executor. The executor sends conversation messages to a fixed language model, receives a JSON action, dispatches tools, and appends their observations. Instructions and skills change request content; workflow settings can require checks before completion.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="175" width="655" height="225" rx="14" fill="#e8ede6" stroke="#91a69b"/>
<text x="40" y="202" style="font-size:18px">PARTICIPANT-WRITTEN EXECUTOR · frozen before the comparison</text>
<rect x="40" y="232" width="280" height="75" rx="8" fill="#d9e6ef"/>
<text x="58" y="261" style="font-size:22px">my_dispatch(name, …)</text><text x="58" y="290" style="font-size:20px">calls the selected Python tool</text>
<rect x="355" y="232" width="300" height="75" rx="8" fill="#dce8df"/>
<text x="373" y="261" style="font-size:22px">my_observation(…, result)</text><text x="373" y="290" style="font-size:20px">adds the result to messages</text>
<path d="M320 270H350" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<text x="45" y="348" style="font-size:21px">Tools read or change the simulated account.</text>
<text x="45" y="378" style="font-size:19px">Account state stays in Python; returned observations enter the request.</text>
<rect x="850" y="210" width="240" height="128" rx="12" fill="#163c43"/>
<text x="970" y="249" text-anchor="middle" fill="#fff" style="font-size:27px">Fixed model</text><text x="970" y="281" text-anchor="middle" fill="#d8e8e0" style="font-size:21px">chooses a JSON action</text><text x="970" y="311" text-anchor="middle" fill="#d8e8e0" style="font-size:18px">weights unchanged</text>
<path d="M660 242H843" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="754" y="224" text-anchor="middle" style="font-size:19px">messages →</text>
<path d="M970 344V355H735V416H8V270H34" fill="none" stroke="#b6783d" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="905" y="390" text-anchor="middle" style="font-size:19px">action + arguments</text>
<g v-if="level>=1">
<rect x="20" y="10" width="1090" height="130" rx="14" fill="#f3ecd8" stroke="#b8a97d" stroke-dasharray="7 4"/>
<text x="40" y="40" style="font-size:18px">HARNESS CONFIGURATION · the editor can revise these fields</text>
<rect x="40" y="56" width="310" height="65" rx="8" fill="#f1ca70"/><text x="55" y="83" style="font-size:23px">instructions.md</text><text x="55" y="109" style="font-size:19px">task rules in the system request</text>
<path d="M195 124V168" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
</g>
<g v-if="level>=2">
<rect x="370" y="56" width="360" height="65" rx="8" fill="#f1ca70"/><text x="385" y="83" style="font-size:23px">skills/verify-operation.md</text><text x="385" y="109" style="font-size:19px">read_skill returns the procedure</text>
<rect x="750" y="56" width="340" height="65" rx="8" fill="#f1ca70"/><text x="765" y="83" style="font-size:23px">workflow.json</text><text x="765" y="109" style="font-size:19px">read retries + completion guard</text>
<path d="M550 124V168" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><path d="M920 124V151H620V169" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
</g>
<g v-if="level===0"><text x="40" y="60" style="font-size:25px">Customer request: refund Acme’s duplicate payment.</text><text x="40" y="100" style="font-size:22px">The model selects an operation. The executor performs it.</text></g>
</g></svg>
</template>
