<script setup>
import { useId } from 'vue'
const props = defineProps({mode: String, stage: {type:Number, default:0}})
const arrow = `transit-mechanism-${useId()}`
const summary = {
  joins:'Actual MBTA rows join stop_times to trips by trip_id, then trips to the service calendar by service_id. Park Street uses stop_id 70076.',
  'service-day':'Actual trip 63926435 departs at service time 24:08 on November 28, which is civil time 00:08 on November 29. Keep both dates.',
  worker:'Illustrative source flows through reading, a reviewed edit, public tests, and a completion request. The actual tool observation enters the next model request.',
  claim:'The local claim-race check interleaves two workers reading pending before either writes. The repaired store checks and assigns one owner under a lock.',
  copies:'Two directories begin with the same source. Each worker edits only its owned file. Integration checks base hashes, combines reviewed patches, then tests the app.',
  tasks:'A task dependency graph permits independent query and renderer work. Integration waits for both outputs; submission, testing and integration are separate states.',
  records:'Task records track ownership, project contracts define interfaces, and lessons retain an evidence-backed rule with scope and version.',
  memory:'Four illustrative notes are filtered by accepted status, current contract version, scope, and tags. Only the reviewed service-day note reaches the worker context.',
  matched:'Matched follow-up conditions share source, task, model and limits. Only accepted lessons differ. Both R5 follow-ups passed 12 of 18 cases and stopped before completing the query.',
  timezone:'Recorded R5 UTC defect: the same instant is 23:00 UTC and 18:00 Eastern. The team query selects the later service-clock train, and its renderer displays that same wrong trip.',
  outcomes:'R5 one-worker build passed 10 of 10 scenarios in 124.78 seconds; two-worker build passed 8 of 10 in 94.91 seconds. Builder time excludes human review and integration.'
}
const notes = [
  {title:'Unreviewed guess',status:'proposed',scope:'transit',version:'v1',tag:'service-day'},
  {title:'Old interface rule',status:'accepted',scope:'transit',version:'v0',tag:'service-day'},
  {title:'Billing retry rule',status:'accepted',scope:'billing',version:'v1',tag:'refund'},
  {title:'Keep the service date',status:'accepted',scope:'transit',version:'v1',tag:'service-day'},
]
</script>
<template>
<svg class="transit-mechanism" viewBox="0 0 1120 375" role="img" :aria-label="summary[mode]" :style="{'--tip':`url(#${arrow})`}">
<defs><marker :id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#61746e"/></marker></defs>
<template v-if="mode==='joins'">
  <text x="18" y="24" class="eyebrow">ACTUAL ROWS · MBTA ARCHIVE 20241128</text>
  <text x="18" y="62" class="title">stop_times</text><path d="M18 75H445" class="rule"/>
  <text x="22" y="104" class="small">trip_id</text><text x="160" y="104" class="small">stop_id</text><text x="285" y="104" class="small">departure_time</text>
  <rect x="15" y="116" width="430" height="49" class="paper"/><rect x="16" y="116" width="137" height="49" class="blue"/>
  <text x="25" y="148" class="code">63926435</text><text x="170" y="148" class="code">70076</text><text x="295" y="148" class="code">24:08:00</text>
  <g v-if="stage>=1">
    <path d="M85 166V196H558V166" class="arrow"/>
    <text x="272" y="221" class="small">match trip_id</text>
    <text x="500" y="62" class="title">trips</text><path d="M500 75H1100" class="rule"/>
    <text x="510" y="104" class="small">trip_id</text><text x="660" y="104" class="small">service_id</text><text x="920" y="104" class="small">headsign</text>
    <rect x="500" y="116" width="600" height="49" class="paper"/><rect x="500" y="116" width="142" height="49" class="blue"/><rect x="647" y="116" width="254" height="49" class="gold"/>
    <text x="510" y="148" class="code">63926435</text><text x="658" y="148" class="code">ThanksgivingDay</text><text x="932" y="148" class="code">Alewife</text>
  </g>
  <g v-if="stage>=2">
    <path d="M775 166V249" class="arrow"/><text x="795" y="221" class="small">match service_id</text>
    <rect x="500" y="254" width="600" height="96" class="paper"/><text x="520" y="284" class="title">Service calendar + exceptions</text><text x="520" y="323" class="code">ThanksgivingDay → active on 2024-11-28</text>
  </g>
  <g><path d="M210 166V251H36V279" class="arrow"/><text x="20" y="304" class="small">stops[70076]</text><text x="20" y="337" class="title">Park Street · Alewife-bound</text></g>
</template>
<template v-else-if="mode==='service-day'">
  <text x="18" y="25" class="eyebrow">TRIP 63926435 · PARK STREET · ACTUAL TIMESTAMPS</text>
  <text x="18" y="76" class="big">24:08:00</text><text x="295" y="64" class="title">24 hours + 8 minutes</text><text x="295" y="96" class="small">elapsed from the service-day origin</text>
  <path d="M65 182H1060" class="axis"/>
  <g v-for="n in [0,6,12,18,24]" :key="n"><path :d="`M${65+n*37.5} 174v16`" class="rule"/><text :x="65+n*37.5" y="219" text-anchor="middle" class="small">{{n}} h</text></g>
  <circle cx="65" cy="182" r="8" class="parent-fill"/><text x="18" y="143" class="title">Nov 28 · 00:00</text>
  <g v-if="stage>=1"><path d="M65 182H965" class="elapsed"/><text x="380" y="157" class="title">One whole service day</text><path d="M965 126V236" class="dashed"/><text x="860" y="110" class="title">Nov 29 · 00:00</text></g>
  <g v-if="stage>=2"><circle cx="1015" cy="182" r="9" class="orange-fill"/><path d="M965 182H1015" class="late"/><text x="905" y="261" class="title">00:08 boarding</text><text x="570" y="316" class="code">boarding: Nov 29 00:08 -05:00</text></g>
  <text x="18" y="316" class="code">service_date: 2024-11-28</text>
  <text x="18" y="357" class="small">Hours preserve duration. Keep the original service date in the returned record. Last 8 minutes enlarged.</text>
</template>
<template v-else-if="mode==='worker'">
  <text x="18" y="24" class="eyebrow">ILLUSTRATIVE EDIT · ACTUAL WORKER TOOL CONTRACT</text>
  <g v-for="(label,i) in ['read_file','write_file','run_tests','finish']" :key="label">
    <circle :cx="55+i*275" cy="65" r="20" :class="i===stage?'blue':'paper'"/><text :x="55+i*275" y="72" text-anchor="middle" class="small">{{i+1}}</text><text :x="85+i*275" y="73" class="code">{{label}}</text>
    <path v-if="i<3" :d="`M${235+i*275} 65h55`" class="arrow"/>
  </g>
  <path d="M20 125H665V330H20Z" class="paper"/><path d="M20 125H665V167H20Z" class="blue"/>
  <text x="40" y="153" class="code">query.py</text><text x="400" y="153" class="small">{{stage===0?'read source + hash':'current working copy'}}</text>
  <text x="40" y="200" class="code">hours, minutes, _ = value.split(":")</text>
  <text v-if="stage===0" x="40" y="242" class="code">hour_s = int(hours) % 24 * 3600</text>
  <g v-if="stage>=1"><rect x="29" y="211" width="627" height="33" class="orange"/><text x="40" y="235" class="code">− hour_s = int(hours) % 24 * 3600</text><rect x="29" y="248" width="627" height="33" class="blue"/><text x="40" y="272" class="code">+ hour_s = int(hours) * 3600</text></g>
  <text x="40" y="310" class="code">seconds = hour_s + int(minutes) * 60</text>
  <path d="M665 219H719" class="arrow"/>
  <text x="745" y="152" class="eyebrow">TOOL OBSERVATION</text>
  <text x="745" y="192" class="title">{{stage===0?'text + before_sha256':stage===1?'new source hash':stage===2?'24:08 remains tomorrow':'Patch awaits review'}}</text>
  <text x="745" y="230" class="small">{{stage===0?'Use this hash in the edit.':stage===1?'Old test receipt cleared.':stage===2?'Current source tested.':'No automatic release.'}}</text>
  <text x="745" y="266" class="code">{{stage===2?'24 × 3600 + 8 × 60':stage===3?'status: review':'observation: result'}}</text>
  <path v-if="stage<3" d="M880 292V346H65V330" class="arrow dashed"/>
  <text v-if="stage<3" x="250" y="369" class="small">Append this returned value to the next model request.</text>
  <text v-else x="20" y="355" class="small">A changed file invalidates earlier passing tests. Human review and integration still follow.</text>
</template>
<template v-else-if="mode==='claim'">
  <text x="18" y="24" class="eyebrow">DETERMINISTIC LOCAL CHECK · TWO THREADS · NO MODEL CALLS</text>
  <text x="18" y="80" class="title">Worker A</text><text x="18" y="161" class="title">Task store</text><text x="18" y="244" class="title">Worker B</text>
  <path d="M170 72H1090M170 154H1090M170 236H1090" class="lane"/>
  <g v-if="stage<2">
    <path d="M240 72V154M385 236V154" class="arrow"/><text x="190" y="56" class="code">read</text><text x="335" y="274" class="code">read</text>
    <rect x="190" y="128" width="250" height="50" class="paper"/><text x="210" y="160" class="code">status: pending</text>
    <g v-if="stage>=1"><path d="M610 72V154M820 236V154" class="arrow"/><text x="555" y="56" class="code">assign A</text><text x="762" y="274" class="code">assign B</text><text x="496" y="193" class="small">The reads did not reserve the task.</text><text x="875" y="345" class="title">2 workers start</text></g>
  </g>
  <g v-else>
    <rect x="212" y="103" width="380" height="103" class="blue"/><text x="235" y="135" class="eyebrow">LOCK HELD</text><text x="235" y="167" class="code">check pending → owner=A</text><path d="M260 72V103" class="arrow"/><text x="220" y="56" class="code">claim</text>
    <path d="M710 236V154" class="arrow"/><text x="650" y="274" class="code">claim</text><text x="630" y="135" class="code">already owned</text><text x="850" y="345" class="title">1 worker starts</text>
  </g>
  <path d="M180 315H1075" class="arrow"/><text x="190" y="346" class="small">Event order →</text><text v-if="stage===2" x="410" y="346" class="small">Release the lock before inference.</text>
</template>
<template v-else-if="mode==='copies'">
  <text x="18" y="25" class="eyebrow">ILLUSTRATIVE PATCHES · IMPLEMENTED OWNERSHIP AND HASH CHECKS</text>
  <path d="M20 100V260H230V100Z" class="paper"/><path d="M20 100V78H130L150 100" class="outline-edge"/><text x="38" y="131" class="title">Start</text><text x="38" y="175" class="code">query.py</text><text x="38" y="212" class="code">presentation.py</text>
  <path d="M230 154C265 154 265 82 308 82M230 216C265 216 265 273 308 273" class="arrow"/>
  <rect x="310" y="47" width="345" height="100" class="blue"/><text x="331" y="78" class="title">Worker A · query.py</text><text x="331" y="116" class="code">{{stage===0?'Same initial source':'+ preserve service_date'}}</text>
  <rect x="310" y="225" width="345" height="100" class="orange"/><text x="331" y="256" class="title">Worker B · presentation.py</text><text x="331" y="294" class="code">{{stage===0?'Same initial source':'+ show departure_time'}}</text>
  <g v-if="stage>=1"><text x="330" y="184" class="small">Each patch records its original file hash.</text></g>
  <g v-if="stage>=2"><path d="M655 95C700 95 700 142 750 142M655 275C700 275 700 200 750 200" class="arrow"/><path d="M755 89H1098V263H755Z" class="paper"/><text x="775" y="125" class="title">Combined app</text><text x="775" y="169" class="code">query → renderer</text><text x="775" y="209" class="small">Run integration checks.</text><text x="755" y="309" class="small">Changed base? Stop with a conflict.</text></g>
  <text x="18" y="366" class="small">Separate folders protect unfinished work. They are not security sandboxes.</text>
</template>
<template v-else-if="mode==='tasks'">
  <text x="18" y="25" class="eyebrow">ILLUSTRATIVE TASK DEPENDENCIES · STATUS HAS TO JUSTIFY THE NEXT ACTION</text>
  <rect x="18" y="131" width="225" height="83" class="paper"/><text x="38" y="167" class="title">Feature contract</text><text x="38" y="198" class="small">Approved inputs + outputs</text>
  <path d="M243 167C290 167 290 83 345 83M243 183C290 183 290 266 345 266" class="arrow"/>
  <rect x="348" y="42" width="325" height="96" class="blue"/><text x="370" y="77" class="title">Return departures</text><text x="370" y="116" class="code">query.py · {{stage?'integrated':'pending'}}</text>
  <rect x="348" y="220" width="325" height="96" class="orange"/><text x="370" y="255" class="title">Render the board</text><text x="370" y="294" class="code">presentation.py · {{stage?'integrated':'pending'}}</text>
  <path d="M673 89C713 89 713 155 768 155M673 267C713 267 713 193 768 193" class="arrow"/>
  <rect x="770" y="129" width="330" height="95" :class="stage?'blue':'paper'"/><text x="792" y="167" class="title">Check combined app</text><text x="792" y="204" class="code">{{stage?'ready to run':'blocked: needs both outputs'}}</text>
  <text x="20" y="366" class="small">pending → running → review → integrated. Review requires passing tests on the current source.</text>
</template>
<template v-else-if="mode==='records'">
  <text x="18" y="24" class="eyebrow">ILLUSTRATIVE RECORD CONTENTS · THREE DIFFERENT QUESTIONS</text>
  <g v-for="(label,i) in ['TASK BOARD','PROJECT CONTRACT','CHECKED LESSON']" :key="label"><path :d="`M${18+i*375} 58h320l28 28v245h-348Z`" class="paper"/><path :d="`M${338+i*375} 58v28h28`" class="outline-edge"/><text :x="38+i*375" y="100" class="eyebrow">{{label}}</text></g>
  <text x="38" y="144" class="title">Who owns this work?</text><text x="38" y="192" class="code">task: departures</text><text x="38" y="226" class="code">owner: worker-a</text><text x="38" y="260" class="code">status: review</text><text x="38" y="305" class="small">Resume this build.</text>
  <text x="413" y="144" class="title">What must agree?</text><text x="413" y="192" class="code">departure_time: ISO</text><text x="413" y="226" class="code">service_date: date</text><text x="413" y="260" class="code">order: ascending</text><text x="413" y="305" class="small">Connect query to renderer.</text>
  <text x="788" y="144" class="title">What can be reused?</text><text x="788" y="192" class="code">Keep hours above 24.</text><text x="788" y="226" class="code">scope: transit · v1</text><text x="788" y="260" class="code">evidence: test + trace</text><text x="788" y="305" class="small">Help a later task.</text>
</template>
<template v-else-if="mode==='memory'">
  <text x="18" y="23" class="eyebrow">ILLUSTRATIVE NOTES · FILTER BEFORE FILLING THE WORKER’S CONTEXT</text>
  <g v-for="(note,i) in notes" :key="note.title">
    <path :d="`M18 ${43+i*75}h650v63H18Z`" :class="i===3?'blue':'paper'"/>
    <text x="34" :y="69+i*75" class="title">{{note.title}}</text><text x="34" :y="94+i*75" class="small">{{note.status}} · {{note.scope}} · {{note.version}} · {{note.tag}}</text>
    <g v-if="i<3 && stage>i"><path :d="`M700 ${57+i*75}l18 18m-18 0l18 -18`" class="cross"/><text x="735" :y="76+i*75" class="small">{{['Not reviewed','Wrong version','Wrong scope / tags'][i]}}</text></g>
  </g>
  <g v-if="stage>=3"><path d="M668 300H740" class="arrow"/><text x="765" y="284" class="title">Next worker request</text><text x="765" y="322" class="code">lessons: [this rule]</text></g>
  <text x="18" y="366" class="small">A recorded read proves consultation. The next patch and its tests show what the worker did.</text>
</template>
<template v-else-if="mode==='matched'">
  <text x="18" y="24" class="eyebrow">MATCHED FOLLOW-UPS · ONLY THE ACCEPTED LESSON INPUT DIFFERS</text>
  <rect x="18" y="48" width="1082" height="55" class="paper"/><text x="37" y="83" class="code">Same starting code · same work order · same model · same request limits</text>
  <text x="20" y="153" class="title">Without lessons</text><text x="20" y="197" class="code">memory: []</text><text x="20" y="271" class="title">With checked lesson</text><text x="20" y="315" class="code">memory: [reviewed rule]</text>
  <g v-if="stage<2"><path d="M300 170H390M300 290H390" class="arrow"/><g v-for="y in [170,290]" :key="y"><circle cx="425" :cy="y" r="28" class="blue"/><circle cx="500" :cy="y" r="28" class="orange"/><text x="425" :y="y+7" text-anchor="middle" class="small">A</text><text x="500" :y="y+7" text-anchor="middle" class="small">B</text><path v-if="stage>=1" :d="`M540 ${y}H650`" class="arrow"/><text v-if="stage>=1" x="675" :y="y+7" class="title">Own patches + independent checks</text></g></g>
  <g v-else><g v-for="y in [176,294]" :key="y"><g v-for="n in 18" :key="n"><rect :x="360+(n-1)*31" :y="y-22" width="24" height="28" :class="n<=12?'blue':'paper'"/></g><text x="950" :y="y+2" class="title">12 / 18</text></g><text x="360" y="221" class="small">212.88 s · $0.02565 · stopped at input bound.</text><text x="360" y="339" class="small">96.13 s · $0.01600 · stopped at output bound.</text></g>
  <text x="18" y="368" class="small">{{stage===2?'Recorded R5: equal scores; neither query change completed. No demonstrated memory benefit.':'Fresh task boards and conversations. Keep both attempts, including unfinished work.'}}</text>
</template>
<template v-else-if="mode==='timezone'">
  <text x="18" y="24" class="eyebrow">RECORDED R5 · CLOCK REPRESENTATIONS · SPACING ILLUSTRATIVE</text>
  <text x="18" y="74" class="title">UTC</text><text x="18" y="166" class="title">Eastern</text><path d="M200 65H1080M200 157H1080" class="axis"/>
  <g v-for="(x,i) in [235,625,1015]" :key="x"><path :d="`M${x} 55v112`" class="dashed"/><text :x="x" y="44" text-anchor="middle" class="code">{{['23:00','23:03','04:03 next day'][i]}}</text><text :x="x" y="194" text-anchor="middle" class="code">{{['18:00','18:03','23:03'][i]}}</text></g>
  <circle cx="235" cy="65" r="9" class="parent-fill"/><circle cx="625" cy="157" r="9" class="blue-fill"/>
  <text x="165" y="233" class="small">Rider asks now</text><text x="445" y="233" class="title">Expected trip 63919613</text>
  <g v-if="stage>=1"><circle cx="1015" cy="157" r="9" class="orange-fill"/><text x="792" y="266" class="title">Team selects 63919759</text><text x="792" y="298" class="small">Later service-clock 23:03</text></g>
  <g v-if="stage>=2"><path d="M220 320H730" class="arrow"/><text x="20" y="319" class="small">Wrong query</text><text x="750" y="326" class="title">Same wrong train on the board</text></g>
  <text x="18" y="368" class="small">Two failed cases: departures/utc-input and integrated/departures/utc-input. One underlying defect.</text>
</template>
<template v-else-if="mode==='outcomes'">
  <text x="18" y="23" class="eyebrow">RECORDED R5 · PRODUCT QUALITY AND BUILDER TIME</text>
  <text x="250" y="63" class="title">Final scenarios passed</text><text x="760" y="63" class="title">Builder elapsed</text>
  <text x="18" y="126" class="title">One worker</text><text x="18" y="223" class="title">Two workers</text>
  <g v-for="(row,i) in [{pass:10,sec:124.78,cost:'0.01107'},{pass:8,sec:94.91,cost:'0.01221'}]" :key="i">
    <g v-for="n in 10" :key="n"><rect :x="250+(n-1)*32" :y="102+i*97" width="25" height="30" :class="n<=row.pass?'blue':'paper'"/></g><text x="590" :y="126+i*97" class="title">{{row.pass}} / 10</text>
    <rect x="760" :y="104+i*97" :width="row.sec*2" height="24" :class="i?'orange':'blue'"/><text x="760" :y="160+i*97" class="small">{{row.sec}} s · ${{row.cost}}</text>
  </g>
  <text x="18" y="316" class="title">The team finished its builder work sooner, but selected the wrong train in two final checks.</text>
  <text x="18" y="357" class="small">One paired rehearsal. Time excludes human review and integration; cost includes this build’s model requests.</text>
</template>
</svg>
</template>
<style scoped>
.transit-mechanism{width:100%;height:375px;margin:4px 0}.paper{fill:#eceee3;stroke:#a9b7a8}.blue{fill:#d6e7ee;stroke:#4382a6}.orange{fill:#f0dfce;stroke:#c17b40}.gold{fill:#f5e4ab;stroke:#b99d46}.title{font:500 22px 'IBM Plex Sans';fill:#163c43}.big{font:500 46px 'IBM Plex Mono';fill:#163c43}.small{font:19px 'IBM Plex Sans';fill:#365d55}.code{font:18px 'IBM Plex Mono';fill:#163c43}.eyebrow{font:14px 'IBM Plex Mono';fill:#61746e;letter-spacing:.45px}.rule,.outline-edge{fill:none;stroke:#61746e;stroke-width:1.7}.axis,.lane{fill:none;stroke:#a9b7a8;stroke-width:2}.arrow{fill:none;stroke:#61746e;stroke-width:2.5;marker-end:var(--tip)}.dashed{fill:none;stroke:#61746e;stroke-width:2;stroke-dasharray:6 6}.elapsed{fill:none;stroke:#4382a6;stroke-width:5}.late{stroke:#c17b40;stroke-width:6}.blue-fill{fill:#4382a6}.orange-fill{fill:#c17b40}.parent-fill{fill:#61746e}.cross{stroke:#9b6339;stroke-width:3}
</style>
