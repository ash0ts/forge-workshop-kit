<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
defineProps({level:{default:1}})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 425" role="img" aria-label="Two proposals start from the participant's manual harness and its starting run. Candidate A retains it; candidate B requires check_work. Each probe resets the account to case.initial. Compose reads both executions and returns a harness to test. The depicted candidate changes come from the recorded first-round proposals; participant proposals may differ.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="12" y="146" width="196" height="124" rx="9" fill="#dce8df"/><text x="30" y="177" style="font-size:23px">Manual harness</text><text x="30" y="210" style="font-size:19px">+ its starting run</text><text x="30" y="244" style="font-size:18px">shared by A and B</text>
<path d="M210 184C235 184 225 90 274 90" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><path d="M210 231C235 231 225 317 274 317" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="282" y="47" width="250" height="86" rx="9" fill="#d9e6ef"/><text x="300" y="80" style="font-size:20px">A · Retain the procedure</text><text x="300" y="112" style="font-size:20px">same harness content</text>
<rect x="282" y="274" width="250" height="86" rx="9" fill="#edcdaa"/><text x="300" y="307" style="font-size:20px">B · Require check_work</text><text x="300" y="339" style="font-size:20px">completion guard → true</text>
<g v-if="level>=2"><path d="M537 90H565" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><path d="M537 317H565" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="574" y="47" width="200" height="86" rx="9" fill="#d9e6ef"/><text x="591" y="79" style="font-size:23px">Probe A</text><text x="591" y="111" style="font-size:19px">start: refunds []</text>
<rect x="574" y="274" width="200" height="86" rx="9" fill="#edcdaa"/><text x="591" y="307" style="font-size:23px">Probe B</text><text x="591" y="339" style="font-size:19px">start: refunds []</text>
<text x="295" y="189" font-family="IBM Plex Mono" style="font-size:20px">deepcopy(case.initial)</text><text x="295" y="220" style="font-size:19px">No refund or message history passes A → B.</text></g>
<g v-if="level>=3"><path d="M780 89C820 89 802 165 829 165" fill="none" stroke="#7d968b" stroke-width="3" stroke-dasharray="6 4" :marker-end="`url(#${arrow})`"/><path d="M780 317C818 317 802 235 829 235" fill="none" stroke="#7d968b" stroke-width="3" stroke-dasharray="6 4" :marker-end="`url(#${arrow})`"/>
<rect x="837" y="140" width="270" height="123" rx="9" fill="#f1ca70"/><text x="855" y="173" style="font-size:24px">Compose</text><text x="855" y="206" style="font-size:18px">read both execution records</text><text x="855" y="239" style="font-size:20px">select / combine / retain</text></g>
<g v-if="level>=4"><path d="M971 269V297" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="837" y="305" width="270" height="62" rx="9" fill="#dce8df"/><text x="855" y="331" style="font-size:21px">Test selected harness</text><text x="855" y="356" style="font-size:18px">reset this case once more</text></g>
<text x="12" y="410" style="font-size:17px">Example candidates from the recorded billing round. Solid arrows pass configurations; dashed arrows pass execution records.</text>
</g></svg>
</template>
