<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism compact" viewBox="0 0 1120 230" role="img" aria-label="The executed operation returns a result to the caller and a saved record for instrumentation. my_tool_span exports the saved record to Agent Lens. Retrying export reads the saved record without rerunning the operation.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="15" y="45" width="220" height="100" rx="9" fill="#dce8df"/><text x="35" y="79" style="font-size:23px">Run the operation</text><text x="35" y="113" style="font-size:21px">inspect_notebook</text>
<path d="M240 72H290V30H480" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="495" y="38" style="font-size:22px">result → notebook output</text>
<path d="M241 112H337" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="345" y="70" width="380" height="92" rx="9" fill="#f3e4b7"/><text x="365" y="103" style="font-size:23px">Saved record</text><text x="365" y="135" style="font-size:19px">arguments · result · timing · error</text>
<path d="M730 112H852" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="790" y="91" text-anchor="middle" style="font-size:18px">my_tool_span</text>
<rect x="860" y="70" width="240" height="92" rx="9" fill="#d9e6ef"/><text x="885" y="108" style="font-size:23px">Agent Lens span</text><text x="885" y="139" style="font-size:19px">same observed operation</text>
<path d="M980 168V197H540V169" fill="none" stroke="#b6783d" stroke-width="2.5" stroke-dasharray="6 4" :marker-end="`url(#${arrow})`"/><text x="742" y="218" text-anchor="middle" style="font-size:18px">Export retry reads the saved record.</text>
</g></svg>
</template>
