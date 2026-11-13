<script setup>
const examples=[['Full refund',[4900],true],['Partial refund',[100],false],['False completion',[],false],['Duplicate refund',[4900,4900],false]]
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 420" role="img" aria-label="Four public development checks all use the reply Everything is resolved. Their refund amounts are 4900, 100, none, and 4900 twice. my_state_check passes only the one full refund. These are deterministic local test fixtures, not LLM judge results.">
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="12" width="1080" height="55" rx="8" fill="#f3e4b7"/><text x="40" y="47" style="font-size:24px">The reply is identical in every example: “Everything is resolved.”</text>
<text x="30" y="109" style="font-size:18px">PUBLIC DEVELOPMENT FIXTURE</text><text x="390" y="109" style="font-size:18px">REFUNDS IN THE ACCOUNT</text><text x="845" y="109" style="font-size:18px">my_state_check</text>
<g v-for="(item,i) in examples" :key="item[0]" :transform="`translate(0,${i*65})`">
<path d="M20 124H1100" stroke="#b4c3b6"/><text x="30" y="161" style="font-size:24px">{{item[0]}}</text>
<rect v-for="(amount,j) in item[1]" :key="j" :x="390+j*145" y="136" width="133" height="42" rx="6" :fill="item[2]?'#c4ddd0':'#edcdaa'"/>
<text v-for="(amount,j) in item[1]" :key="'amount'+j" :x="456+j*145" y="164" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:22px">{{amount}} ¢</text>
<text v-if="!item[1].length" x="410" y="162" font-family="IBM Plex Mono" style="font-size:22px">[]</text>
<text x="845" y="161" style="font-size:25px">{{item[2]?'PASS':'FAIL'}}</text>
<text x="930" y="161" style="font-size:19px">{{item[2]?'one full refund':'wrong state'}}</text>
</g>
<text x="22" y="412" style="font-size:18px">Deterministic free checks from teaching.check_scorer. No model judgment is shown or assumed.</text>
</g></svg>
</template>
