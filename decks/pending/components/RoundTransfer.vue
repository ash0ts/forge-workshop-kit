<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
defineProps({recorded:Boolean})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 430" role="img" :aria-label="recorded?'Recorded round one kept the manual harness; round two used it on a newly reset onboarding case, then revised the verification skill. The agent model stayed fixed.':'The selected harness, lesson, limits, and source execution are saved together. The next round runs that harness on a new case and sends its fresh execution plus the earlier lesson to the editor. Account state does not transfer across cases.'">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="30" width="280" height="164" rx="10" fill="#d9e6ef"/><text x="40" y="66" style="font-size:25px">Round 1 · Billing</text><text x="40" y="104" style="font-size:18px">propose → probe → compose</text><text x="40" y="142" style="font-size:21px">{{recorded?'Retain manual harness':'Test the selected harness'}}</text><text x="40" y="175" style="font-size:19px">{{recorded?'5cfd358201e0':'Reflect on that execution'}}</text>
<path d="M308 115H359" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="367" y="30" width="365" height="164" rx="10" fill="#f3e4b7"/><text x="387" y="66" style="font-size:25px">Saved together</text><text x="387" y="105" font-family="IBM Plex Mono" style="font-size:21px">harness + fingerprint</text><text x="387" y="137" font-family="IBM Plex Mono" style="font-size:21px">lesson + limits</text><text x="387" y="169" font-family="IBM Plex Mono" style="font-size:21px">source execution</text>
<path d="M739 115H790" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="798" y="30" width="302" height="164" rx="10" fill="#dce8df"/><text x="818" y="66" style="font-size:25px">Round 2 · Onboarding</text><text x="818" y="105" style="font-size:21px">run the selected harness</text><text x="818" y="137" style="font-size:21px">on the new account state</text><text x="818" y="169" style="font-size:19px">then propose and test again</text>
<path d="M950 201V245H727" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="367" y="222" width="350" height="133" rx="10" fill="#f1ca70"/><text x="387" y="256" style="font-size:23px">Editor receives two sources</text><text x="387" y="291" style="font-size:20px">current onboarding execution</text><text x="387" y="326" style="font-size:20px">earlier billing lesson + limits</text>
<path d="M550 201V216" stroke="#b6783d" stroke-width="3" stroke-dasharray="6 4"/>
<text x="20" y="267" style="font-size:20px">Account state resets.</text><text x="20" y="299" style="font-size:20px">Billing refunds do not</text><text x="20" y="331" style="font-size:20px">enter the onboarding case.</text>
<g v-if="recorded"><text x="799" y="269" style="font-size:21px">Recorded next selection:</text><text x="799" y="303" style="font-size:21px">exactly-once verification skill</text><text x="799" y="337" style="font-size:20px">completion gate stays off</text></g>
<text x="22" y="414" style="font-size:18px">If the selected execution is incomplete, carry the parent harness instead. Adoption here is not an automatic best-score ranking.</text>
</g></svg>
</template>
