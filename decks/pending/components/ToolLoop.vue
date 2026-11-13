<script setup>
import {useId} from 'vue'
const arrow = useId().replace(/:/g,'')
defineProps({level:{default:1}})
</script>
<template>
<svg style="width:100%;height:auto;max-height:400px" viewBox="0 0 1100 390" role="img" aria-label="The agent requests an invoice. Dispatch calls Python. Its returned payments become an observation in the next model request.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="65" width="230" height="110" rx="12" fill="#dce8df"/>
<text x="40" y="100" style="font-size:24px">1 · Model request</text><text x="40" y="135" style="font-size:19px">Refund the duplicate</text><text x="40" y="159" style="font-size:19px">on Acme invoice inv-1.</text>
<g v-if="level>=2"><path d="M255 120H305" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="315" y="65" width="260" height="110" rx="12" fill="#f1ca70"/><text x="335" y="100" style="font-size:24px">2 · Chosen action</text><text x="335" y="135" style="font-size:19px">lookup_invoice</text><text x="335" y="159" style="font-size:19px">acme · inv-1</text></g>
<g v-if="level>=3"><path d="M580 120H630" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="640" y="65" width="435" height="110" rx="12" fill="#d9e6ef"/><text x="660" y="100" style="font-size:24px">3 · my_dispatch → my_invoice_tool</text><text x="660" y="135" style="font-size:19px">Read the selected account’s payments.</text><text x="660" y="159" style="font-size:19px">The lookup does not change its state.</text></g>
<g v-if="level>=4"><path d="M850 181V230" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="640" y="240" width="435" height="105" rx="12" fill="#dce8df"/><text x="660" y="275" style="font-size:24px">4 · Returned observation</text><text x="660" y="310" style="font-size:20px">pay-1: $49 · pay-2: $49 · no refunds</text></g>
<g v-if="level>=5"><path d="M635 291H290" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="450" y="270" text-anchor="middle" style="font-size:20px">my_observation appends it</text>
<rect x="20" y="240" width="260" height="105" rx="12" fill="#163c43"/><text x="40" y="276" fill="#fff" style="font-size:24px">5 · Next request</text><text x="40" y="311" fill="#c8ddd3" style="font-size:19px">Now it can use those facts.</text></g>
</g>
</svg>
</template>
