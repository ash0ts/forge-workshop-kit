<script setup>
import { computed } from 'vue'
import windowData from '../data/teaching-window.json'
import qualification from '../data/qualification-summary.json'
const props = defineProps({ mode: String, reveal: { type: Number, default: 3 } })
const w = windowData
const points = (fn, x0, x1, y0, sx, sy) => Array.from({length:121}, (_,i) => {
  const x=x0+(x1-x0)*i/120; return `${70+(x-x0)*sx},${y0-fn(x)*sy}`
}).join(' ')
const seedRows = computed(() => qualification.seeds.map(seed => ({seed,
  before: qualification.rows.find(r=>r.task==='images' && r.recipe==='manual' && r.seed===seed).error,
  after: qualification.rows.find(r=>r.task==='images' && r.recipe==='zero_residual' && r.seed===seed).error,
})))
const descriptions = {
  normalize:'One measured XRS-B value changes coordinate systems: log-flux minus the training mean, divided by the training standard deviation. The target stays in log-flux units.',
  error:'The prediction and observed target occupy different positions on a log-flux axis. Their distance is the absolute forecast error.',
  alignment:'Matching column vectors compare one forecast to one target. Dropping the target axis broadcasts every forecast against every target.',
  loss:'Squared loss grows quadratically while absolute loss grows linearly. Their derivatives give different update signals for large residuals.',
  zero:'A zero-initialized residual output head starts at persistence. Its weights learn first; gradients reach earlier features once the head is nonzero.',
  repetition:'Three paired seed results compare the same fixed image recipes. Two improve and one slightly regresses. Overlapping forecast windows are not independent trials.',
  search:'Six configurations compare MLP and CNN architecture, width and learning rate. This is a fixed search over existing implementations, not agent-written code.',
  validation:'Training computes gradients and changes weights. Validation uses those weights without updating them, then produces a score used to choose a version.',
}
</script>

<template>
<svg class="solar-worked" viewBox="0 0 1120 320" role="img" :aria-label="descriptions[mode]">
  <title>{{ descriptions[mode] }}</title>
  <g v-if="mode==='normalize'">
    <text x="20" y="28" class="label">SAME OBSERVATION · 01:00 UTC</text>
    <text x="20" y="72" class="value">{{ w.raw_flux.toExponential(4) }} W/m²</text>
    <path d="M270 63 H340 m-12 -8 l12 8 -12 8" class="arrow"/>
    <text x="285" y="52" class="small">log₁₀</text>
    <text x="370" y="72" class="value">{{ w.latest_log10.toFixed(6) }}</text>
    <g v-if="reveal>=2">
      <text x="20" y="121" class="small">Log-flux axis</text>
      <path d="M190 150 H1000" class="axis"/>
      <g v-for="(v,i) in [-6.02,-5.745,-5.47,-5.195,-4.92]" :key="i">
        <path :d="`M${220+i*180} 143 v14`" class="axis"/><text :x="220+i*180" y="182" text-anchor="middle" class="small">{{ v.toFixed(3) }}</text>
      </g>
      <path d="M580 130 v100" class="dashed"/><text x="580" y="119" text-anchor="middle" class="small">training mean</text>
      <circle cx="538" cy="150" r="8" class="teal"/>
    </g>
    <g v-if="reveal>=3">
      <path d="M190 235 H1000" class="axis"/>
      <g v-for="(v,i) in [-2,-1,0,1,2]" :key="i"><path :d="`M${220+i*180} 228 v14`" class="axis"/><text :x="220+i*180" y="266" text-anchor="middle" class="small">{{ v }}</text></g>
      <circle cx="538" cy="235" r="8" class="teal"/>
      <text x="20" y="239" class="small">Model input</text><text x="735" y="220" class="small">1 unit = {{ w.std_xrsb.toFixed(6) }} log-flux</text>
      <text x="685" y="67" class="value">z = {{ w.standardized_latest.toFixed(6) }}</text>
      <text x="685" y="94" class="small">0.23 standard deviations below the mean.</text>
    </g>
  </g>
  <g v-else-if="mode==='error'">
    <text x="20" y="28" class="label">ONE REAL FORECAST · 2014-02-01</text>
    <path d="M95 188 H1010" class="axis"/>
    <g v-for="(v,i) in [-5.6,-5.4,-5.2,-5.0,-4.8]" :key="i"><path :d="`M${130+i*200} 180 v16`" class="axis"/><text :x="130+i*200" y="226" text-anchor="middle">{{ v.toFixed(1) }}</text></g>
    <circle cx="196" cy="188" r="10" class="blue"/>
    <text x="196" y="107" text-anchor="middle">Persistence prediction</text><text x="196" y="139" text-anchor="middle" class="mono">{{ w.latest_log10.toFixed(6) }}</text>
    <g v-if="reveal>=2"><circle cx="789" cy="188" r="10" class="teal"/><text x="789" y="107" text-anchor="middle">Observed at 01:30</text><text x="789" y="139" text-anchor="middle" class="mono">{{ w.target_log10.toFixed(6) }}</text></g>
    <g v-if="reveal>=3"><path d="M196 65 H789 M196 57 v16 M789 57 v16" class="orange-line"/><text x="490" y="46" text-anchor="middle" class="value">{{ Math.abs(w.latest_log10-w.target_log10).toFixed(6) }}</text><text x="490" y="274" text-anchor="middle" class="small">Absolute error is a distance in log₁₀ flux units, not a percentage.</text></g>
  </g>
  <g v-else-if="mode==='alignment'">
    <text x="20" y="24" class="label">ILLUSTRATIVE TWO-FORECAST BATCH</text>
    <text x="40" y="67">Prediction (2, 1)</text><text x="315" y="67">Target (2, 1)</text>
    <g v-for="(v,i) in [1,3]" :key="i"><rect x="90" :y="95+i*67" width="75" height="54" class="soft"/><text x="127" :y="130+i*67" text-anchor="middle">{{ v }}</text><rect x="370" :y="95+i*67" width="75" height="54" class="soft"/><text x="407" :y="130+i*67" text-anchor="middle">{{ i===0 ? 2 : 5 }}</text><path :d="`M185 ${122+i*67} H348`" class="arrow"/><text x="265" :y="112+i*67" text-anchor="middle" class="small">same case</text></g>
    <text x="65" y="258" class="mono">paired errors = [1, 2]</text>
    <g v-if="reveal>=2"><path d="M530 52 V270" class="dashed"/><text x="590" y="67">Target (2,) broadcasts across columns</text><text x="826" y="100" class="small">2</text><text x="911" y="100" class="small">5</text><text x="750" y="143" class="small">1</text><text x="750" y="205" class="small">3</text>
      <g v-for="(v,i) in [1,4,1,2]" :key="i"><rect :x="790+(i%2)*85" :y="110+Math.floor(i/2)*62" width="80" height="57" :class="i===0||i===3?'soft':'warn'"/><text :x="830+(i%2)*85" :y="147+Math.floor(i/2)*62" text-anchor="middle">{{v}}</text></g>
    </g>
    <text v-if="reveal>=3" x="595" y="258" class="small">Four differences. Two compare the wrong cases.</text>
  </g>
  <g v-else-if="mode==='loss'">
    <text x="20" y="24" class="label">ILLUSTRATIVE RESIDUALS · e = PREDICTION − TARGET</text>
    <path d="M70 255 H570 M70 255 V52" class="axis"/>
    <g v-for="n in [0,1,2,3]" :key="n"><text :x="70+n*150" y="280" text-anchor="middle" class="small">{{n}}</text></g>
    <text x="320" y="310" class="small">Absolute residual |e|</text><text x="0" y="55" class="small">Loss</text>
    <g v-for="v in [0,3,9]" :key="v"><path :d="`M64 ${255-v*21} h6`" class="axis"/><text x="53" :y="261-v*21" text-anchor="end" class="small">{{v}}</text></g>
    <polyline :points="points(x=>x*x,0,3,255,150,21)" class="orange-line"/><text x="458" y="48" class="small">e²</text>
    <g v-if="reveal>=2"><polyline :points="points(x=>x,0,3,255,150,21)" class="teal-line"/><text x="535" y="195" class="small">|e|</text></g>
    <g v-if="reveal>=3"><text x="640" y="70">At e = 3</text><text x="640" y="119" class="orange-text">Squared loss = 9 · gradient = 6</text><text x="640" y="163" class="teal-text">Absolute loss = 3 · gradient = 1</text><path d="M640 190 H1080" class="axis"/><text x="640" y="228" class="small">Large errors pull harder under squared loss.</text><text x="640" y="259" class="small">The fixed evaluation metric remains absolute error.</text></g>
  </g>
  <g v-else-if="mode==='zero'">
    <text x="20" y="25" class="label">ILLUSTRATIVE ONE-FEATURE RESIDUAL HEAD</text>
    <text x="65" y="80" class="mono">feature h = 2</text><path d="M260 75 H350 m-12 -8 l12 8 -12 8" class="arrow"/>
    <text x="385" y="80" class="mono">head weight w = 0</text><path d="M660 75 H760 m-12 -8 l12 8 -12 8" class="arrow"/>
    <text x="790" y="80" class="mono">correction wh = 0</text>
    <text x="65" y="127" class="small">forecast = current image + 0 → starts at persistence</text>
    <g v-if="reveal>=2"><path d="M1030 155 H385 m12 -8 l-12 8 12 8" class="orange-line"/><text x="640" y="190" class="mono">∂loss/∂w = g × h</text><text x="640" y="222" class="small">The nonzero feature can update the head.</text><path d="M340 155 H65" class="dashed"/><path d="M330 142 v26" class="orange-line"/><text x="65" y="190" class="mono">∂loss/∂h = g × 0</text><text x="65" y="222" class="small">Earlier layers receive zero on this first pass.</text></g>
    <text v-if="reveal>=3" x="65" y="280" class="teal-text">After w changes, gradients can also reach the earlier layers. g is the output gradient.</text>
  </g>
  <g v-else-if="mode==='repetition'">
    <text x="20" y="25" class="label">RECORDED IMAGE RETEST · SAME DATES, THREE SEEDS</text>
    <text x="20" y="67" class="small">Seed</text><text x="440" y="67" class="small">Masked image MAE · lower is better ←</text>
    <path d="M270 240 H1030" class="axis"/>
    <g v-for="v in [0.108,0.112,0.116,0.120,0.124]" :key="v"><path :d="`M${270+(v-.108)*45000} 235 v10`" class="axis"/><text :x="270+(v-.108)*45000" y="273" text-anchor="middle" class="small">{{v.toFixed(3)}}</text></g>
    <g v-for="(r,i) in seedRows" :key="r.seed"><text x="35" :y="107+i*50">{{r.seed}}</text><circle :cx="270+(r.before-.108)*45000" :cy="100+i*50" r="7" class="blue"/><g v-if="reveal>=2"><path :d="`M${270+(r.before-.108)*45000} ${100+i*50} H${270+(r.after-.108)*45000}`" class="arrow"/><circle :cx="270+(r.after-.108)*45000" :cy="100+i*50" r="7" class="orange"/></g><text v-if="reveal>=3" x="108" :y="107+i*50" class="small">{{r.after<r.before?'lower error':'slightly higher'}}</text></g>
    <circle cx="690" cy="25" r="6" class="blue"/><text x="704" y="31" class="small">Manual</text><circle cx="850" cy="25" r="6" class="orange"/><text x="864" y="31" class="small">Agent recipe</text>
  </g>
  <g v-else-if="mode==='validation'">
    <text x="20" y="24" class="label">ONE VERSION OF THE FORECASTING MODEL</text>
    <text x="25" y="72">Training batch</text><text x="25" y="202">Validation batch</text>
    <path d="M205 65 H300 M205 195 H300" class="arrow"/>
    <rect x="315" y="38" width="190" height="56" class="soft"/><text x="410" y="74" text-anchor="middle">weights θ₀</text>
    <g v-if="reveal>=2"><path d="M520 65 H630 m-12 -8 l12 8 -12 8" class="arrow"/><text x="550" y="44" class="small">fit</text><rect x="650" y="38" width="190" height="56" class="soft"/><text x="745" y="74" text-anchor="middle">weights θ₁</text><text x="875" y="73" class="small">optimizer.step()</text><path d="M745 100 V145 H410 V165" class="arrow"/></g>
    <g v-if="reveal>=3"><rect x="315" y="168" width="190" height="56" class="soft"/><text x="410" y="204" text-anchor="middle">weights θ₁</text><path d="M520 195 H630 m-12 -8 l12 8 -12 8" class="arrow"/><text x="660" y="204">Prediction → fixed score</text><path d="M410 230 V260 H875" class="dashed"/><text x="900" y="267" class="small">θ₁ unchanged</text><text x="25" y="284" class="small">Selecting a version from validation scores is a separate decision.</text></g>
  </g>
  <g v-else-if="mode==='search'">
    <text x="20" y="25" class="label">SIX FIXED CONFIGURATIONS · NOT EVERY POSSIBLE COMBINATION</text>
    <text x="300" y="69" text-anchor="middle">Reference setting</text><text x="610" y="69" text-anchor="middle">More hidden features</text><text x="940" y="69" text-anchor="middle">Larger learning rate</text>
    <text x="20" y="135">MLP</text><text x="20" y="222">CNN</text>
    <g v-for="(setting,i) in [{width:16,lr:'.001'},{width:32,lr:'.001'},{width:16,lr:'.003'}]" :key="i">
      <g v-if="reveal>=i+1" v-for="r in [0,1]" :key="r">
        <rect :x="180+i*320" :y="94+r*87" width="270" height="63" class="soft"/>
        <g v-for="j in (setting.width===16?4:8)" :key="j"><circle :cx="198+i*320+j*10" :cy="116+r*87" r="3" class="teal"/></g>
        <text :x="295+i*320" :y="121+r*87" class="small">width {{setting.width}}</text>
        <text :x="198+i*320" :y="146+r*87" class="mono">learning rate {{setting.lr}}</text>
      </g>
    </g>
    <text x="180" y="286" class="small">All six use seed 17, batch size 32, and 60 updates. The data and metric stay fixed.</text>
  </g>
</svg>
</template>

<style scoped>
.solar-worked{width:100%;height:320px;display:block;margin:10px 0 16px;overflow:visible}
text{font:23px 'IBM Plex Sans',sans-serif;fill:#163c43}.label{font-size:16px;letter-spacing:1px;fill:#61746e}.small{font-size:18px}.value{font-size:26px;font-weight:500}.mono{font:21px 'IBM Plex Mono',monospace}
.axis{fill:none;stroke:#9aaea3;stroke-width:1.5}.arrow{fill:none;stroke:#426a6b;stroke-width:2}.dashed{fill:none;stroke:#8c9e98;stroke-width:2;stroke-dasharray:5 5}.orange-line{fill:none;stroke:#c17b40;stroke-width:3}.teal-line{fill:none;stroke:#237a6c;stroke-width:3}.soft{fill:#dce8dd;stroke:#7c9e92}.warn{fill:#f4decb;stroke:#c17b40}.teal{fill:#237a6c}.blue{fill:#4382a6}.orange{fill:#c17b40}.orange-text{fill:#ad642c}.teal-text{fill:#237a6c}
</style>
