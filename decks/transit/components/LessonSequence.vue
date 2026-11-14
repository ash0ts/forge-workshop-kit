<script setup>
import { useId } from "vue"
const arrowId = `lesson-arrow-${useId()}`
defineProps({ mode: {type:String,required:true}, stage: {type:Number,default:0} })
</script>
<template>
<svg class="lesson-sequence" viewBox="0 0 1120 340" :style="{'--lesson-arrow': `url(#${arrowId})`}" role="img" :aria-label="`${mode} teaching sequence, step ${stage + 1}. See the adjacent explanation for the values and decision.`">
<defs><marker :id="arrowId" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#61746e"/></marker></defs>
<template v-if="mode==='service-day'">
  <rect x="0" y="20" width="320" height="152" class="parent"/><text x="22" y="54" class="label">STOP TIMES</text><text x="22" y="91" class="main">Trip 63926435 · stop 70076</text><text x="22" y="126" class="mono">departure_time: 24:08:00</text><text x="22" y="155" class="small">Park Street → Alewife</text>
  <g v-if="stage>=1"><path d="M320 95H378" class="wire"/><rect x="380" y="20" width="330" height="152" class="blue"/><text x="402" y="54" class="label">TRIP + ACTIVE SERVICE</text><text x="402" y="91" class="main">ThanksgivingDay</text><text x="402" y="126" class="mono">service_date: 2024-11-28</text><text x="402" y="155" class="small">Keep this date in the result</text></g>
  <g v-if="stage>=2"><path d="M710 95H768" class="wire"/><rect x="770" y="20" width="350" height="152" class="orange"/><text x="792" y="54" class="label">CIVIL TIMESTAMP</text><text x="792" y="91" class="main">November 29 · 00:08</text><text x="792" y="126" class="mono">2024-11-29T00:08:00-05:00</text><text x="792" y="155" class="small">The rider boards on Friday</text></g>
  <path d="M50 265H1070" class="timeline"/><circle cx="90" cy="265" r="7" fill="#4382a6"/><text x="45" y="235" class="small">Nov 28 · 00:00</text><text x="45" y="306" class="small">Service-day origin</text>
  <g v-if="stage>=2"><circle cx="900" cy="265" r="7" fill="#61746e"/><text x="780" y="235" class="small">Nov 29 · 00:00</text><circle cx="1030" cy="265" r="9" fill="#c17b40"/><text x="945" y="306" class="small">+24 h 8 min</text><path d="M900 265H1030" stroke="#c17b40" stroke-width="5"/></g>
</template>
<template v-else-if="mode==='worker'">
  <rect x="0" y="45" width="245" height="150" class="blue"/><text x="20" y="80" class="label">MODEL ACTION</text><text x="20" y="120" class="main">{{stage===0?'read_file':stage===1?'write_file':stage===2?'run_tests':'finish'}}</text><text x="20" y="157" class="mono">{{stage===0?'query.py':stage===1?'path + hash + content':stage===2?'current working copy':'reason + test record'}}</text>
  <path d="M245 120H300" class="wire"/><rect x="302" y="45" width="245" height="150" class="parent"/><text x="322" y="80" class="label">PYTHON TOOL</text><text x="322" y="120" class="main">{{stage===0?'Read owned source':stage===1?'Check the old hash':stage===2?'Run public checks':'Validate completion'}}</text><text x="322" y="157" class="small">{{stage===0?'Return text + SHA256':stage===1?'Then write the new file':stage===2?'Record actual output':'Current code must pass'}}</text>
  <path d="M547 120H602" class="wire"/><rect x="604" y="45" width="245" height="150" class="orange"/><text x="624" y="80" class="label">OBSERVATION</text><text x="624" y="120" class="main">{{stage===0?'Source and hash':stage===1?'New source hash':stage===2?'Pass or error':'Patch awaits review'}}</text><text x="624" y="157" class="small">Saved before continuing</text>
  <path d="M849 120H900" class="wire"/><rect x="902" y="45" width="218" height="150" class="parent"/><text x="922" y="80" class="label">NEXT STEP</text><text x="922" y="120" class="main">{{stage===3?'Human review':'Model request'}}</text><text x="922" y="157" class="small">{{stage===3?'No automatic release':'Includes the result'}}</text>
  <path v-if="stage<3" d="M1005 195V270H122V195" class="wire evidence"/>
  <text x="240" y="310" class="small">Solid arrows: execution. Dashed return: observation supplied as context.</text>
</template>
<template v-else-if="mode==='claim'">
  <rect x="0" y="30" width="265" height="90" class="blue"/><text x="22" y="67" class="main">Worker A</text><text x="22" y="99" class="small">Wants query.py</text>
  <rect x="0" y="205" width="265" height="90" class="orange"/><text x="22" y="242" class="main">Worker B</text><text x="22" y="274" class="small">Also sees the task</text>
  <path d="M265 75H380V150H440" class="wire"/><path d="M265 250H380V175H440" class="wire"/>
  <rect x="442" y="90" width="315" height="150" class="parent"/><text x="464" y="128" class="label">{{stage===2?'LOCKED TRANSACTION':'SHARED TASK'}}</text><text x="464" y="166" class="main">{{stage===2?'Check + assign owner':'status: pending'}}</text><text x="464" y="207" class="small">{{stage===2?'Release lock before model call':'Two readers can see this'}}</text>
  <g v-if="stage>=1"><path d="M757 165H815" class="wire"/><rect x="817" y="90" width="303" height="150" :class="stage===1?'orange':'blue'"/><text x="839" y="128" class="label">LOCAL TWO-THREAD CHECK</text><text x="839" y="171" class="large">{{stage===1?'2 owners':'1 owner'}}</text><text x="839" y="211" class="small">{{stage===1?'Both started the same task':'Other claimant gets no claim'}}</text></g>
</template>
<template v-else-if="mode==='copies'">
  <rect x="0" y="105" width="220" height="125" class="parent"/><text x="20" y="144" class="main">Starting source</text><text x="20" y="180" class="mono">query.py</text><text x="20" y="208" class="mono">presentation.py</text>
  <path d="M220 165C260 165 260 77 310 77" class="wire"/><path d="M220 165C260 165 260 257 310 257" class="wire"/>
  <rect x="312" y="15" width="310" height="125" class="blue"/><text x="334" y="54" class="main">Worker A's copy</text><text x="334" y="89" class="mono">{{stage===0?'Same initial files':'Edits query.py only'}}</text><text x="334" y="120" class="small">{{stage===0?'Separate directory':'Own checks + proposed patch'}}</text>
  <rect x="312" y="200" width="310" height="125" class="orange"/><text x="334" y="239" class="main">Worker B's copy</text><text x="334" y="274" class="mono">{{stage===0?'Same initial files':'Edits presentation.py only'}}</text><text x="334" y="305" class="small">{{stage===0?'Separate directory':'Own checks + proposed patch'}}</text>
  <g v-if="stage>=2"><path d="M622 77C685 77 675 150 740 150" class="wire"/><path d="M622 257C685 257 675 185 740 185" class="wire"/><rect x="742" y="100" width="378" height="140" class="parent"/><text x="764" y="138" class="main">Review, apply, test together</text><text x="764" y="176" class="small">Check each patch's base hash</text><text x="764" y="211" class="small">Then test query → renderer → app</text></g>
</template>
<template v-else-if="mode==='memory'">
  <g v-for="(item,index) in [{title:'Unchecked interpretation',status:'proposed',scope:'transit',version:'transit-v1',tag:'service-day'},{title:'Rule for the old interface',status:'accepted',scope:'transit',version:'transit-v0',tag:'service-day'},{title:'Rule for billing retries',status:'accepted',scope:'billing',version:'transit-v1',tag:'refund'},{title:'Reviewed service-day rule',status:'accepted',scope:'transit',version:'transit-v1',tag:'service-day'}]" :key="item.title">
    <rect x="0" :y="10+index*80" width="640" height="68" :class="index===3?'blue':'parent'" :opacity="(stage>=1&&index===0)||(stage>=2&&index===1)||(stage>=3&&index===2)?0.4:1"/>
    <text x="18" :y="38+index*80" class="main">{{item.title}}</text><text x="18" :y="63+index*80" class="small">{{item.status}} · {{item.scope}} · {{item.version}} · {{item.tag}}</text>
    <text v-if="stage>=1&&index===0" x="670" :y="50+index*80" class="small">Exclude: not reviewed</text>
    <text v-if="stage>=2&&index===1" x="670" :y="50+index*80" class="small">Exclude: old contract version</text>
    <text v-if="stage>=3&&index===2" x="670" :y="50+index*80" class="small">Exclude: wrong scope and tags</text>
    <text v-if="stage>=3&&index===3" x="670" :y="50+index*80" class="main">Supply this rule and its evidence</text>
  </g>
</template>
<template v-else-if="mode==='matched'">
  <rect x="0" y="95" width="270" height="145" class="parent"/><text x="20" y="135" class="main">One selected starting build</text><text x="20" y="173" class="small">Same source + work order</text><text x="20" y="209" class="small">Same model + request limits</text>
  <path d="M270 165C315 165 310 78 370 78" class="wire"/><path d="M270 165C315 165 310 257 370 257" class="wire"/>
  <rect x="372" y="15" width="360" height="125" class="blue"/><text x="394" y="53" class="main">Two workers without lessons</text><text x="394" y="89" class="mono">memory: []</text><text x="394" y="119" class="small">Fresh task board and conversations</text>
  <rect x="372" y="200" width="360" height="125" class="orange"/><text x="394" y="238" class="main">Two workers with the lesson</text><text x="394" y="274" class="mono">memory: [reviewed rule]</text><text x="394" y="304" class="small">Fresh task board and conversations</text>
  <g v-if="stage>=1"><path d="M732 78H780" class="wire"/><path d="M732 257H780" class="wire"/><rect x="782" y="15" width="338" height="125" class="parent"/><rect x="782" y="200" width="338" height="125" class="parent"/><text x="804" y="57" class="main">{{stage===1?'Own patches + checks':'R5: 12 / 18 final cases'}}</text><text x="804" y="99" class="small">{{stage===1?'Preserve incomplete work too':'Query stopped at input bound'}}</text><text x="804" y="242" class="main">{{stage===1?'Own patches + checks':'R5: 12 / 18 final cases'}}</text><text x="804" y="284" class="small">{{stage===1?'Do not edit the lesson mid-pair':'Query exhausted output limit'}}</text></g>
</template>
<template v-else-if="mode==='timezone'">
  <rect x="0" y="15" width="335" height="135" class="parent"/><text x="22" y="54" class="label">THE SAME INSTANT</text><text x="22" y="94" class="main">23:00 UTC = 18:00 Eastern</text><text x="22" y="129" class="small">The feed uses America/New_York</text>
  <path d="M335 83H390" class="wire"/><rect x="392" y="15" width="330" height="135" class="blue"/><text x="414" y="54" class="label">FEED-TIMEZONE ORIGIN</text><text x="414" y="94" class="main">18:03 Eastern</text><text x="414" y="129" class="mono">trip 63919613</text>
  <g v-if="stage>=1"><path d="M170 150V230H390" class="wire"/><rect x="392" y="175" width="330" height="135" class="orange"/><text x="414" y="214" class="label">CALLER-TIMEZONE ORIGIN</text><text x="414" y="254" class="main">Service-clock 23:03</text><text x="414" y="289" class="mono">trip 63919759</text></g>
  <g v-if="stage>=2"><path d="M722 242H775" class="wire"/><rect x="777" y="175" width="343" height="135" class="parent"/><text x="799" y="214" class="label">TWO FAILED CHECKS</text><text x="799" y="254" class="main">Wrong query → wrong board</text><text x="799" y="289" class="small">One underlying timezone defect</text></g>
</template>
</svg>
</template>
<style scoped>
.lesson-sequence{width:100%;height:340px;margin:8px 0}.parent{fill:#e6e8dd;stroke:#a9b7a8}.blue{fill:#d6e7ee;stroke:#4382a6}.orange{fill:#f0dfce;stroke:#c17b40}rect{rx:7}.main{font:500 22px 'IBM Plex Sans';fill:#163c43}.large{font:600 36px 'IBM Plex Sans';fill:#163c43}.small{font:18px 'IBM Plex Sans';fill:#365d55}.mono{font:16px 'IBM Plex Mono';fill:#163c43}.label{font:14px 'IBM Plex Mono';fill:#61746e;letter-spacing:.5px}.wire{fill:none;stroke:#61746e;stroke-width:2.5;marker-end:var(--lesson-arrow)}.evidence{stroke-dasharray:7 5}.timeline{stroke:#a9b7a8;stroke-width:3}
</style>
