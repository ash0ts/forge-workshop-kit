<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 415" role="img" aria-label="Expected outcome for the fictional Acme duplicate-charge fixture. Before: captured payments pay-1 and pay-2 for invoice inv-1, each 4900 cents, and no refunds. After: both payment records remain, with exactly one 4900-cent refund for pay-2. The other account is unchanged.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="31" style="font-size:25px">Before · Acme</text><text x="640" y="31" style="font-size:25px">Expected after · Acme</text>
<rect x="20" y="52" width="460" height="239" rx="10" fill="#e8ede6"/><rect x="640" y="52" width="460" height="239" rx="10" fill="#e8ede6"/>
<g v-for="x in [40,660]" :key="x"><text :x="x" y="90" style="font-size:21px">Payments on inv-1</text><text :x="x" y="133" font-family="IBM Plex Mono" style="font-size:23px">pay-1 · 4900¢ · captured</text><text :x="x" y="174" font-family="IBM Plex Mono" style="font-size:23px">pay-2 · 4900¢ · captured</text></g>
<text x="40" y="252" font-family="IBM Plex Mono" style="font-size:24px">refunds: []</text>
<rect x="653" y="209" width="433" height="62" rx="7" fill="#bcdcca"/><text x="670" y="248" font-family="IBM Plex Mono" style="font-size:23px">refunds: [pay-2 · 4900¢]</text>
<path d="M486 172H632" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="559" y="137" text-anchor="middle" style="font-size:20px">refund</text><text x="559" y="205" text-anchor="middle" style="font-size:20px">pay-2 once</text>
<rect x="20" y="318" width="1080" height="53" rx="8" fill="#f3e4b7"/><text x="40" y="352" style="font-size:23px">Preserve pay-1, all unrelated records, and the other customer’s account.</text>
<text x="22" y="406" style="font-size:18px">Expected fixture state. Code checks the account; an LLM judge checks the reply against recorded actions.</text>
</g></svg>
</template>
