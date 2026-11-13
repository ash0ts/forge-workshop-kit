<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
defineProps({level:{default:1}})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 430" role="img" aria-label="Illustrative invoice lookup: the model returns action lookup_invoice with account_id acme and invoice_id inv-1. my_dispatch passes those arguments to my_invoice_tool. Its result contains pay-1 and pay-2 at 4900 cents each. my_observation appends the action and result to the next request.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="10" y="16" width="265" height="158" rx="10" fill="#dce8df"/>
<text x="28" y="48" style="font-size:23px">1 · Model input</text><text x="28" y="85" style="font-size:21px">Refund the duplicate</text><text x="28" y="115" style="font-size:21px">on Acme invoice inv-1.</text><text x="28" y="154" style="font-size:18px">+ instructions + tool guide</text>
<g v-if="level>=2"><path d="M278 92H313" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="320" y="16" width="335" height="158" rx="10" fill="#f1ca70"/>
<text x="338" y="48" style="font-size:23px">2 · JSON response</text><g font-family="IBM Plex Mono" style="font-size:19px"><text x="338" y="84">action: "lookup_invoice"</text><text x="338" y="116">account_id: "acme"</text><text x="338" y="148">invoice_id: "inv-1"</text></g></g>
<g v-if="level>=3"><path d="M659 92H694" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="700" y="16" width="410" height="158" rx="10" fill="#d9e6ef"/>
<text x="718" y="48" style="font-size:23px">3 · Dispatch in Python</text><g font-family="IBM Plex Mono" style="font-size:20px"><text x="718" y="83">my_invoice_tool(</text><text x="742" y="115">world, "acme", "inv-1"</text><text x="718" y="147">)</text></g></g>
<g v-if="level>=4"><path d="M904 180V218" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="700" y="225" width="410" height="164" rx="10" fill="#dce8df"/>
<text x="718" y="258" style="font-size:23px">4 · Python return value</text><g font-family="IBM Plex Mono" style="font-size:19px"><text x="718" y="294">payments: [pay-1, pay-2]</text><text x="718" y="326">amount_cents: 4900 each</text><text x="718" y="358">refunds: []</text></g></g>
<g v-if="level>=5"><path d="M694 305H631" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="10" y="225" width="615" height="164" rx="10" fill="#163c43"/>
<text x="28" y="258" fill="#fff" style="font-size:23px">5 · my_observation builds the next request</text><g font-family="IBM Plex Mono" fill="#dce8df" style="font-size:19px"><text x="28" y="294">previous messages</text><text x="28" y="326">+ assistant: JSON action with acme / inv-1</text><text x="28" y="358">+ user: Tool observation: {payments, refunds}</text></g></g>
<text x="12" y="420" style="font-size:17px">Illustration from the public invoice fixture. Field labels abbreviate JSON; the next code slide shows the exact message format.</text>
</g></svg>
</template>
