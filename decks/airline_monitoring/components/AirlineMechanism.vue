<script setup>
import { computed, useId } from 'vue'
import qualification from '../data/qualification.json'
const props = defineProps({ mode: String, reveal: { type: Number, default: 1 } })
const r = computed(() => props.reveal)
const markerId = `airline-arrow-${useId().replace(/[^a-z0-9_-]/gi, '')}`
const finalCases = qualification.runs.filter(run => run.split === 'final' && run.label === 'baseline').map(run => ({
  id: run.case_id,
  baseline: run.scores.task_success,
  repaired: qualification.runs.find(other => other.case_id === run.case_id && other.label === 'repaired')?.scores.task_success,
}))
const score = (split, label) => {
  const row = qualification.summary[`${split}/${label}`]
  return `${row.task_successes}/${row.executions}`
}
const descriptions = {
  replacement: 'Reservation 59XX6W contains HAT007 outward and HAT174 return. Sending only HAT061 replaces the entire list and removes HAT174. Sending HAT061 and HAT174 preserves the return.',
  families: 'Keep all related passenger and reservation tasks in one partition before running qualification. Discovery has eight requests, monitor check four, development four paired, final six paired, and later traffic four paired.',
  loop: 'A passenger request enters model messages. The chosen update action becomes Python arguments. The returned booking is appended as a tool observation before the next model request.',
  spans: 'One conversation contains a turn with sibling model and tool spans. The tool error, retry, and returned reservation have distinct events and recorded timing. This is a schematic, not measured durations.',
  context: 'The full conversation may contain the original booking in an earlier turn. A later turn may contain only an approval, write, and result. A turn-level judge cannot infer missing original state.',
  criteria: 'Alignment tests a draft against human-reviewed turns. Live traffic continues using saved criteria until the reviewed draft is explicitly saved. Testing and saving are separate operations.',
  nonstop: 'An illustrative three-segment round trip has two connecting outward flights and one return. The approved nonstop replaces both outward flights. The return remains, so fewer flights is not a failure.',
  confusion: 'Illustrative reviewed processed sample: three true positives, one false positive, one false negative, three true negatives. Precision divides three by four alerts; recall divides three by four reviewed failures.',
  precision: 'Illustrative precision: the four alerted turns contain three reviewed failures and one false positive. Precision is three quarters. Unalerted turns are outside this denominator.',
  recall: 'Illustrative recall: the four reviewed failures contain three alerted turns and one missed failure. Recall is three quarters. Reviewed nonfailures are outside this denominator.',
  coverage: 'Illustrative ten eligible turns: eight completed predictions and two unavailable. Coverage is eight tenths. Only completed, reviewed predictions enter the confusion matrix.',
  missing: 'An absent live tag has three possible interpretations: a completed negative judgment, processing pending, or a failed/unavailable judgment. Positive assignments alone cannot distinguish them.',
  curation: 'A reviewed incident is reconstructed from request, original booking, policy, expected behavior, review decision, and source identities. The saved case starts from the original booking, never the mutated result.',
  slice: 'Illustrative array: outbound-1 and outbound-2 occupy indices zero and one; return-1 occupies index two. Replace the half-open range zero to two. Concatenate empty prefix, new-outbound, and untouched return-1.',
  matched: 'Each reserved request is cloned into identical initial states. Starting and repaired code execute independently. Compare the resulting bookings on the same case, and retain unavailable judgments as missing.',
  results: 'Recorded final results: the starting and repaired agents each passed all six task checks; both passed all four subsequent requests. Native monitor accuracy remains unavailable.',
}
const matrix = [
  { x: 280, y: 80, n: 3, label: 'True positive', cls: 'teal' },
  { x: 555, y: 80, n: 1, label: 'False positive', cls: 'amber' },
  { x: 280, y: 205, n: 1, label: 'False negative', cls: 'amber' },
  { x: 555, y: 205, n: 3, label: 'True negative', cls: 'pale' },
]
</script>

<template>
<svg class="airline-mechanism" viewBox="0 0 1160 405" role="img" :aria-label="descriptions[mode]" :style="{'--airline-arrow': `url(#${markerId})`}">
  <defs><marker :id="markerId" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#47776d" /></marker></defs>

  <g v-if="mode === 'replacement'">
    <text x="10" y="30" class="label">CURRENT RESERVATION 59XX6W</text>
    <path d="M165 75H655" class="route"/><circle cx="165" cy="75" r="7"/><circle cx="655" cy="75" r="7"/>
    <text x="165" y="115" text-anchor="middle">LAS</text><text x="655" y="115" text-anchor="middle">ATL</text>
    <text x="410" y="60" text-anchor="middle" class="mono">HAT007 · May 19</text>
    <path d="M655 155H165" class="arrow muted-line"/><text x="410" y="190" text-anchor="middle" class="mono">HAT174 · May 29 · return</text>
    <g v-if="r >= 2" data-reveal-step="2">
      <path d="M770 20V335" class="divider"/><text x="810" y="42" class="label">API INPUT REPLACES BOTH</text>
      <text x="810" y="100" class="mono">[HAT061]</text><text x="810" y="138" class="warning">Return omitted</text>
      <path d="M815 170L1125 170" class="divider"/>
    </g>
    <g v-if="r >= 3" data-reveal-step="3"><text x="810" y="222" class="mono">[HAT061, HAT174]</text><text x="810" y="260">Return preserved</text>
      <rect x="9" y="239" width="711" height="92" rx="6" class="pale"/><text x="30" y="275" class="mono">reservation.flights = new_flights</text><text x="30" y="310" class="small">This assignment replaces the list; it does not merge it.</text>
    </g><text x="10" y="385" class="small">The omitted-return branch illustrates the API mechanism. It was not observed in the live qualification.</text>
  </g>

  <g v-else-if="mode === 'families'">
    <text x="10" y="30" class="label">RELATED TASK ROWS</text>
    <g v-for="(label,i) in ['Same passenger','Same reservation','Reworded request']" :key="label"><circle cx="45" :cy="84+i*66" r="13" class="teal"/><text x="80" :y="92+i*66">{{label}}</text></g>
    <path d="M350 60H370V240H350" class="bracket"/><text x="392" y="115">One family</text><text x="392" y="150" class="small">assign once</text>
    <g v-if="r >= 2" data-reveal-step="2"><path d="M535 140H600V49H628" class="arrow"/>
      <g v-for="(label,i) in ['Discovery · 8','Monitor check · 4','Development · 4 × 2','Final · 6 × 2','Later traffic · 4 × 2']" :key="label">
        <rect x="640" :y="25+i*61" width="485" height="48" rx="4" :class="i===0?'teal':'pale'"/><text x="665" :y="57+i*61">{{label}}</text>
      </g>
    </g><g v-if="r >= 3" data-reveal-step="3"><path d="M410 216Q550 282 632 230" class="dash"/><path d="M548 235L571 258M571 235L548 258" class="cross"/><text x="10" y="346">Do not send another row from this family to a later group.</text><text x="10" y="386" class="small">Family geometry is illustrative. The five request counts are the frozen workshop assignments.</text></g>
  </g>

  <g v-else-if="mode === 'loop'">
    <g v-for="(label,i) in ['Messages','Fixed model','Python tool','Booking state']" :key="label"><text :x="125+i*290" y="30" text-anchor="middle">{{label}}</text><path :d="`M${125+i*290} 55V330`" class="lifeline"/></g>
    <path d="M125 85H408" class="arrow"/><text x="153" y="73" class="small">request + current booking</text>
    <g v-if="r >= 2" data-reveal-step="2"><path d="M415 150H698" class="arrow"/><text x="446" y="136" class="small">update(..., flights=[...])</text><path d="M705 195H988" class="arrow"/><text x="735" y="181" class="small">replace complete itinerary</text></g>
    <g v-if="r >= 3" data-reveal-step="3"><path d="M995 235H712" class="arrow"/><text x="739" y="266" class="small">returned booking</text><path d="M705 290H132" class="arrow"/><text x="240" y="277" class="small">append tool observation to messages</text></g>
    <g v-if="r >= 4" data-reveal-step="4"><path d="M125 330H408" class="arrow"/><text x="147" y="363" class="small">next request includes the result</text><text x="10" y="400" class="mono small">messages.append({"role": "tool", "content": observation})</text></g>
  </g>

  <g v-else-if="mode === 'spans'">
    <text x="10" y="30" class="label">PARENTAGE</text><text x="595" y="30" class="label">OPERATION ORDER · SCHEMATIC, NOT MEASURED DURATION</text>
    <text x="10" y="78">Conversation</text><path d="M30 90V120H60M85 138V330" class="bracket"/><text x="65" y="130">Turn</text>
    <g v-for="(label,i) in ['Model request','Reservation read: error','Model request','Reservation read: returned']" :key="label">
      <g v-if="r>=Math.min(i+1,3)" :data-reveal-step="Math.min(i+1,3)"><path :d="`M85 ${174+i*52}H115`" class="bracket"/><text x="125" :y="181+i*52" class="small">{{label}}</text><rect :x="595+i*115" :y="157+i*52" width="105" height="24" rx="4" :class="i===1?'amber':'teal'"/></g>
    </g>
    <g v-if="r >= 3"><text x="10" y="386" class="small">Record each operation's arguments, result, error, and actual start/end timestamps. Export time is different.</text></g>
  </g>

  <g v-else-if="mode === 'context'">
    <rect x="10" y="20" width="1130" height="302" rx="7" class="boundary"/><text x="32" y="56" class="label">CONVERSATION</text>
    <text x="40" y="110">Earlier turn</text><text x="40" y="157" class="mono small">Before: [HAT007, HAT174]</text><text x="40" y="199" class="small">Keep the return flight.</text>
    <g v-if="r >= 2" data-reveal-step="2"><rect x="515" y="76" width="590" height="212" rx="5" class="teal"/><text x="540" y="111">Selected turn supplied to the judge</text><text x="540" y="158" class="small">Passenger: Yes, please.</text><text x="540" y="201" class="mono small">After: [HAT061]</text><text x="540" y="246" class="small">Final reply: Your booking is updated.</text></g>
    <g v-if="r >= 3" data-reveal-step="3"><path d="M355 155H505" class="dash"/><path d="M424 143L446 166M446 143L424 166" class="cross"/><text x="10" y="365">The selected turn cannot establish which flight was removed.</text><text x="10" y="399" class="small">Illustrative incomplete context. Review it as insufficient evidence, not a known negative.</text></g>
  </g>

  <g v-else-if="mode === 'criteria'">
    <text x="10" y="32" class="label">ALIGNMENT WORKSPACE</text><text x="770" y="32" class="label">NEW TRAFFIC</text>
    <path d="M720 52V327" class="divider"/><rect x="10" y="70" width="620" height="84" class="pale" rx="6"/><text x="30" y="103">Draft: inspect approved change scope</text><text x="30" y="136" class="small">Experiment criteria and reviewed turns</text>
    <rect x="770" y="70" width="370" height="160" class="teal" rx="6"/><text x="792" y="111">Saved live criteria</text><text x="792" y="157" class="small">Apply with AI enabled</text><text x="792" y="197" class="small">Scoped to this agent</text>
    <g v-if="r >= 2" data-reveal-step="2"><path d="M65 162V205H615" class="arrow"/><text x="92" y="193" class="small">test draft against reviewed turns</text><text x="30" y="255">Prediction, disagreement, or unavailable</text></g>
    <g v-if="r >= 3" data-reveal-step="3"><path d="M625 292H957V240" class="arrow"/><text x="30" y="313" class="mono">Explicit save →</text><text x="10" y="377" class="small">Testing a draft does not update the criteria used on subsequent traffic. Verify the saved snapshot.</text></g>
  </g>

  <g v-else-if="mode === 'nonstop'">
    <text x="10" y="28" class="label">ILLUSTRATIVE APPROVED CHANGE · SAME ORIGIN AND DESTINATION</text>
    <text x="10" y="87">Before</text><path d="M235 82H990" class="route"/><circle cx="235" cy="82" r="8"/><circle cx="610" cy="82" r="8"/><circle cx="990" cy="82" r="8"/>
    <text x="400" y="61" text-anchor="middle" class="small">outbound-1</text><text x="800" y="61" text-anchor="middle" class="small">outbound-2</text><text x="610" y="119" text-anchor="middle" class="small">connection</text>
    <path d="M990 150H235" class="arrow muted-line"/><text x="610" y="185" text-anchor="middle" class="mono small">return-1</text>
    <g v-if="r >= 2" data-reveal-step="2"><text x="10" y="245">Approved</text><path d="M235 240H990" class="route"/><circle cx="235" cy="240" r="8"/><circle cx="990" cy="240" r="8"/><text x="610" y="226" text-anchor="middle" class="small">new-outbound · nonstop</text><path d="M990 298H235" class="arrow muted-line"/><text x="610" y="335" text-anchor="middle" class="mono small">return-1 · unchanged</text></g>
    <g v-if="r >= 3" data-reveal-step="3"><text x="10" y="393">3 flights → 2 flights. The change is correct because its scope was approved.</text></g>
  </g>

  <g v-else-if="['confusion','precision','recall'].includes(mode)">
    <text x="280" y="35" class="small">Reviewer: failure</text><text x="555" y="35" class="small">Reviewer: no failure</text>
    <text x="10" y="145" class="small">Judge: positive</text><text x="10" y="270" class="small">Judge: negative</text>
    <g v-for="(cell,i) in matrix" :key="cell.label" :opacity="(mode==='precision' && i>1)||(mode==='recall' && i%2===1)?0.62:1">
      <rect :x="cell.x" :y="cell.y" width="255" height="110" rx="5" :class="cell.cls"/>
      <g v-if="r >= (mode==='confusion'?Math.min(i+1,3):1)"><text :x="cell.x+20" :y="cell.y+48" class="number">{{cell.n}}</text><text :x="cell.x+20" :y="cell.y+85" class="small">{{cell.label}}</text></g>
    </g>
    <g v-if="mode === 'precision' && r>=2"><path d="M270 72H820V194H270Z" class="boundary bold"/><text x="855" y="116">Alerts</text><text x="855" y="162" class="mono">3 / 4</text><text x="855" y="209" class="number">75%</text></g>
    <g v-if="mode === 'recall' && r>=2"><path d="M270 72H540V322H270Z" class="boundary bold"/><text x="855" y="116">Failures</text><text x="855" y="162" class="mono">3 / 4</text><text x="855" y="209" class="number">75%</text></g>
    <text x="10" y="378" class="small">Illustrative arithmetic, not native workshop results: 8 reviewed turns with completed predictions.</text>
  </g>

  <g v-else-if="mode === 'coverage'">
    <text x="10" y="32" class="label">10 ELIGIBLE TURNS · ILLUSTRATIVE COUNTS</text>
    <g v-for="i in 10" :key="i"><circle :cx="60+(i-1)*113" cy="110" r="37" :class="i<=8?'teal':'unknown'"/><text :x="60+(i-1)*113" y="119" text-anchor="middle" class="mono">{{i<=8?i:'?'}}</text></g>
    <path d="M22 166V183H890V166" class="bracket"/><text x="455" y="221" text-anchor="middle">8 completed predictions</text><text x="1017" y="221" text-anchor="middle" class="small">2 unavailable</text>
    <g v-if="r >= 2" data-reveal-step="2"><text x="10" y="285" class="mono">coverage = 8 / 10 = 0.80</text><path d="M455 238V270H800" class="arrow"/><text x="820" y="278" class="small">join human reviews</text></g>
    <g v-if="r >= 3" data-reveal-step="3"><text x="10" y="352">Agreement uses the completed, reviewed subset.</text><text x="10" y="391" class="small">Pending or failed judgments remain outside the confusion matrix. Report them alongside coverage.</text></g>
  </g>

  <g v-else-if="mode === 'missing'">
    <circle cx="150" cy="180" r="80" class="unknown"/><text x="150" y="172" text-anchor="middle">No tag</text><text x="150" y="204" text-anchor="middle" class="small">on this turn</text>
    <g v-for="(label,i) in ['Completed negative','Still processing','Judge unavailable']" :key="label">
      <g v-if="r>=i+1" :data-reveal-step="i+1"><path :d="`M234 180H395V${65+i*106}H515`" class="arrow"/><circle cx="550" :cy="65+i*106" r="22" :class="i===0?'teal':'unknown'"/><text x="600" :y="73+i*106">{{label}}</text></g>
    </g><text x="10" y="375" class="small">Only an explicit native test result establishes a known prediction. Positive assignments alone cannot.</text>
  </g>

  <g v-else-if="mode === 'curation'">
    <text x="10" y="25" class="label">EXECUTION HISTORY</text><path d="M35 60V300" class="lifeline"/>
    <circle cx="35" cy="84" r="7"/><text x="63" y="92">Before the request</text><text x="63" y="124" class="mono small">[HAT007, HAT174]</text>
    <circle cx="35" cy="210" r="7"/><text x="63" y="218">After the wrong write</text><text x="63" y="250" class="mono small">[HAT061]</text>
    <rect x="605" y="20" width="530" height="328" rx="5" class="pale"/><text x="630" y="55" class="mono">regression_case</text>
    <g v-if="r>=2" data-reveal-step="2"><path d="M345 104H590" class="arrow"/><text x="630" y="103" class="mono small">initial = original_booking</text><text x="630" y="143" class="mono small">request + policy</text><text x="630" y="183" class="mono small">expected = keep HAT174</text></g>
    <g v-if="r>=3" data-reveal-step="3"><path d="M345 232H550" class="dash"/><path d="M450 220L474 244M474 220L450 244" class="cross"/><text x="630" y="235" class="mono small">review + reason</text><text x="630" y="275" class="mono small">conversation / turn / span</text><text x="630" y="315" class="mono small">executed code + dataset version</text></g>
    <text x="10" y="391" class="small">Illustrative omission incident. Replaying its final state would preserve the damage instead of reproducing it.</text>
  </g>

  <g v-else-if="mode === 'slice'">
    <text x="10" y="25" class="label">ILLUSTRATIVE LIST · REPLACE [0&#58;2]</text>
    <g v-for="(label,i) in ['outbound-1','outbound-2','return-1']" :key="label"><text :x="190+i*332" y="64" text-anchor="middle" class="small">index {{i}}</text><rect :x="40+i*332" y="80" width="300" height="60" rx="5" :class="i<2?'amber':'teal'"/><text :x="190+i*332" y="119" text-anchor="middle" class="mono">{{label}}</text></g>
    <path d="M40 152V170H672V152" class="bracket"/><text x="355" y="205" text-anchor="middle" class="small">start 0 included · stop 2 excluded</text>
    <g v-if="r>=2" data-reveal-step="2"><text x="40" y="260" class="mono">[]</text><text x="180" y="260">+</text><rect x="240" y="227" width="365" height="61" rx="5" class="amber"/><text x="422" y="266" text-anchor="middle" class="mono">[new-outbound]</text><text x="635" y="260">+</text><rect x="700" y="227" width="330" height="61" rx="5" class="teal"/><text x="865" y="266" text-anchor="middle" class="mono">[return-1]</text><text x="40" y="322" class="small">prefix</text><text x="345" y="322" class="small">replacement</text><text x="800" y="322" class="small">suffix</text></g>
    <g v-if="r>=3" data-reveal-step="3"><text x="10" y="389" class="mono small">current[:start] + replacement + current[stop:]</text></g>
  </g>

  <g v-else-if="mode === 'matched'">
    <text x="10" y="29" class="label">SAME REQUEST + ORIGINAL BOOKING</text><rect x="10" y="52" width="283" height="261" rx="7" class="pale"/><text x="30" y="94">Reserved case</text><text x="30" y="145" class="small">Initial state</text><text x="30" y="185" class="small">Passenger requirements</text><text x="30" y="225" class="small">Policy</text>
    <g v-if="r>=2" data-reveal-step="2"><path d="M302 180H355V90H455" class="arrow"/><path d="M355 180V270H455" class="arrow"/><text x="478" y="72">Starting source</text><rect x="478" y="88" width="262" height="55" rx="4" class="pale"/><text x="498" y="122" class="small">isolated booking copy</text><text x="478" y="252">Frozen repair source</text><rect x="478" y="268" width="262" height="55" rx="4" class="teal"/><text x="498" y="302" class="small">isolated booking copy</text></g>
    <g v-if="r>=3" data-reveal-step="3"><path d="M755 115H845" class="arrow"/><path d="M755 295H845" class="arrow"/><text x="875" y="114">Final booking A</text><text x="875" y="294">Final booking B</text><path d="M975 139V259" class="dash"/><text x="835" y="195" class="small">align by case ID</text><text x="835" y="230" class="small">score with the same checks</text></g>
    <text x="10" y="389" class="small">A monitor prediction and an explanation judgment remain separate from the booking-state score.</text>
  </g>

  <g v-else-if="mode === 'results'">
    <text x="10" y="29" class="label">RECORDED FINAL EVALUATION · SIX MATCHED REQUESTS</text>
    <text x="10" y="113">Starting</text><text x="10" y="212">Repaired</text>
    <g v-for="(item,i) in finalCases" :key="item.id"><text :x="330+i*130" y="62" text-anchor="middle" class="small">case {{item.id.split('-').at(-1)}}</text><circle :cx="330+i*130" cy="105" r="28" class="pale"/><text :x="330+i*130" y="114" text-anchor="middle">{{item.baseline===true?'✓':item.baseline===false?'×':'?'}}</text><g v-if="r>=2"><circle :cx="330+i*130" cy="205" r="28" class="teal"/><text :x="330+i*130" y="214" text-anchor="middle">{{item.repaired===true?'✓':item.repaired===false?'×':'?'}}</text></g></g>
    <g v-if="r>=3"><text x="10" y="301">Task checks: {{score('final','baseline')}} starting; {{score('final','repaired')}} repaired. Later traffic: {{score('subsequent','baseline')}}; {{score('subsequent','repaired')}}.</text><text x="10" y="347">Native monitor accuracy: unavailable.</text><text x="10" y="391" class="small">The controlled local repair proves the list operation. This live comparison shows a tie, not a quality gain.</text></g>
  </g>
</svg>
</template>

<style scoped>
.airline-mechanism{display:block;width:100%;height:405px;overflow:visible}
text{font:25px 'IBM Plex Sans',sans-serif;fill:#163c43}.label{font:16px 'IBM Plex Mono',monospace;letter-spacing:.8px}.small{font-size:21px}.mono{font-family:'IBM Plex Mono',monospace;font-size:23px}.mono.small{font-size:20px}.number{font-size:40px;font-weight:500}
.teal{fill:#c9e0d8;stroke:#5b9385;stroke-width:1.5}.pale{fill:#e5e9dd;stroke:#91a89b;stroke-width:1.5}.amber{fill:#f1dfb6;stroke:#bc8750;stroke-width:1.5}.unknown{fill:#f6f2e7;stroke:#89988f;stroke-width:2;stroke-dasharray:6 5}.route{stroke:#237a6c;stroke-width:4;fill:none}.arrow{stroke:#47776d;stroke-width:2.5;fill:none;marker-end:var(--airline-arrow)}.muted-line{stroke:#7c8e85}.lifeline{stroke:#afbbb0;stroke-width:1.5;stroke-dasharray:5 6;fill:none}.bracket{stroke:#567d70;stroke-width:2;fill:none}.divider{stroke:#b0bcb0;stroke-width:1.5}.boundary{fill:none;stroke:#567d70;stroke-width:2}.bold{stroke-width:4}.dash{stroke:#9b8a68;stroke-width:2;stroke-dasharray:6 5;fill:none}.cross{stroke:#ad613c;stroke-width:3}.warning{fill:#945b32}
</style>
