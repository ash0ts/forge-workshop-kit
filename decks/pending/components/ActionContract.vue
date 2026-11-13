<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 410" role="img" aria-label="The tool guide declares lookup_invoice and its account_id and invoice_id arguments. The model returns a JSON action. my_dispatch checks its action name and calls my_invoice_tool with the two arguments. Tool observations return to the next model request.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g fill="#163c43" font-family="IBM Plex Sans">
<text x="20" y="28" style="font-size:21px">The model’s tool guide</text><rect x="20" y="46" width="1080" height="63" rx="8" fill="#f3e4b7"/>
<text x="40" y="85" font-family="IBM Plex Mono" style="font-size:23px">lookup_invoice: {account_id, invoice_id} reads invoice payments and refunds.</text>
<path d="M270 115V149" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="20" y="158" width="475" height="208" rx="10" fill="#f1ca70"/>
<text x="40" y="191" style="font-size:23px">Selected action</text><g font-family="IBM Plex Mono" style="font-size:21px"><text x="40" y="231">{"action": "lookup_invoice",</text><text x="40" y="264"> "arguments": {</text><text x="65" y="297">"account_id": "acme",</text><text x="65" y="330">"invoice_id": "inv-1"}}</text></g>
<path d="M503 261H591" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="600" y="158" width="500" height="208" rx="10" fill="#d9e6ef"/>
<text x="620" y="191" style="font-size:23px">my_dispatch receives</text><g font-family="IBM Plex Mono" style="font-size:21px"><text x="620" y="231">name = "lookup_invoice"</text><text x="620" y="264">arguments = {…}</text><text x="620" y="310">invoice_tool(world, **arguments)</text></g>
<text x="22" y="400" style="font-size:18px">This executor uses a JSON action contract in its prompt. Python dispatch connects that contract to executable code.</text>
</g></svg>
</template>
