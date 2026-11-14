<script setup>
import {useId} from 'vue'
import observed from '../data/teaching-window.json'
const props=defineProps({mode:String,reveal:{type:Number,default:4}})
const marker=useId().replace(/:/g,'')
const n=(value,d=3)=>Number(value).toFixed(d)
const descriptions={
 window:'One real GOES example at February 1, 2014 01:00 UTC. Sixty samples per channel become inputs. The latest log XRS-B is the persistence forecast. The 01:30 observation is the target, kept out of inputs.',
 validity:'A forecast window is admitted only when its complete history-to-target interval is continuous and contained in one date partition. A gap or a split boundary rejects the window.',
 batch:'A batch stacks separate forecast windows. The GOES input shape is batch by two channels by sixty samples; the target and forecast shapes are batch by one. Time is not the batch axis.',
 neuron:'Illustrative arithmetic for one linear unit: multiply three inputs by their weights, add a bias, then apply ReLU. The workshop MLP uses 120 inputs for each unit.',
 filter:'A temporal convolution uses the same learned five-position weights for each channel at successive times. It adds the ten products and a bias to make one output feature.',
 gradient:'Illustrative one-parameter model with x=2 and target=3. With weight one, prediction two, squared loss one and gradient minus four, a plain gradient-descent step of size 0.1 changes the weight to 1.4. The workshop uses Adam.',
 image:'Each example has two 64 by 64 images in one batch item. The current image is channel one. A residual network adds one predicted correction image to that current image.',
 averaging:'The public scorer fixture has one included pixel with error one in the first image and four included pixels with error two in the second. Per-image errors are one and two; their equal-image mean is 1.5, not the pooled-pixel mean of 1.8.',
 context:'The research agent receives current source, configuration and validation evidence. Training code receives training inputs and targets. The fixed scorer uses validation targets. Final-test records are excluded from improvement context.',
 selection:'An agent proposes source. Training produces weights and a validation result. The adoption function compares that result with the parent; strictly lower error adopts, while equal, higher or failed results retain the parent.',
}
</script>
<template>
<svg class="solar-concept" viewBox="0 0 1120 385" role="img" :aria-label="descriptions[mode]" :style="{'--arrow':`url(#${marker})`}">
<defs><marker :id="marker" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6" fill="none" stroke="#52776d" stroke-width="1.8"/></marker></defs>
<g v-if="mode==='window'">
 <text x="20" y="25" class="label">OBSERVED EXAMPLE · 1 FEBRUARY 2014 · UTC</text>
 <path d="M30 144H1085" class="axis"/>
 <rect x="45" y="80" width="530" height="125" fill="#dbe6e1"/>
 <text x="65" y="116">XRSA + XRSB · 60 samples each</text><text x="65" y="155" class="mono">00:01 ... 01:00</text>
 <text x="65" y="187" class="small">Both channels describe observations already available.</text>
 <text x="565" y="242" text-anchor="end">Forecast origin: 01:00</text>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M590 144H735" class="arrow"/><circle cx="810" cy="144" r="10" fill="#c17b40"/><text x="810" y="90" text-anchor="middle">Target at 01:30</text><text x="810" y="185" text-anchor="middle" class="mono">{{n(observed.target_log10)}} log-flux</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="300">Persistence forecast</text><text x="320" y="300" class="mono">{{n(observed.latest_log10)}} → {{n(observed.latest_log10)}}</text><text x="30" y="345" class="small">Copy the latest XRS-B reading. The future target only enters the scorer.</text></g>
</g>
<g v-else-if="mode==='validity'">
 <text x="20" y="25" class="label">ILLUSTRATIVE WINDOWS · THE DATE RULE MATCHES THE LOADER</text>
 <rect x="30" y="65" width="580" height="235" fill="#dbe6e1"/><rect x="610" y="65" width="480" height="235" fill="#f5dba0"/>
 <text x="55" y="97">Training dates</text><text x="635" y="97">Validation dates</text>
 <line x1="610" y1="65" x2="610" y2="300" stroke="#163c43" stroke-width="3"/><text x="610" y="335" text-anchor="middle" class="small">February 11, 00:00 UTC</text>
 <path d="M90 143H430" class="axis"/><circle cx="430" cy="143" r="7" fill="#237a6c"/><text x="65" y="178" class="small">Admit: history through target stays in training</text>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M460 210H815" class="axis"/><circle cx="815" cy="210" r="7" fill="#c17b40"/><text x="645" y="249" class="small">Reject: target crosses the boundary</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><path d="M75 262H225M250 262H400" class="axis"/><path d="M226 251L249 274M249 251L226 274" stroke="#9c593c" stroke-width="3"/><text x="35" y="375" class="small">Also reject a gap anywhere from the first history sample through the target.</text></g>
</g>
<g v-else-if="mode==='batch'">
 <text x="20" y="25" class="label">SHAPES OF THE ACTUAL GOES ARRAYS</text>
 <g v-for="i in 3" :key="i" :transform="`translate(${45+i*16} ${65+i*20})`"><rect width="325" height="130" fill="#f6f2e7" stroke="#52776d"/><rect x="18" y="25" width="285" height="24" fill="#8fb2a4"/><rect x="18" y="70" width="285" height="24" fill="#52776d"/></g>
 <text x="85" y="280">One window: [2, 60]</text><text x="85" y="318" class="small">Channels × one-minute samples</text>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M440 178H535" class="arrow"/><text x="560" y="126">Stack B windows</text><text x="560" y="178" class="shape">[B, 2, 60]</text><text x="560" y="220" class="small">Training uses B = 32.</text><text x="560" y="251" class="small">Free shape check uses B = 2.</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><path d="M820 178H875" class="arrow"/><text x="900" y="126">Forecasts</text><text x="900" y="178" class="shape">[B, 1]</text><text x="900" y="220" class="small">One per window</text></g>
 <text x="20" y="375" class="small">A batch is a collection of examples. It does not add future samples to any example.</text>
</g>
<g v-else-if="mode==='neuron'">
 <text x="20" y="25" class="label">ARITHMETIC EXAMPLE · ONE UNIT WITH THREE INPUTS</text>
 <g v-for="(row,i) in [['Input','2','−1','0.5'],['Weight','0.2','−0.3','0.4']]" :key="i"><text x="30" :y="98+i*60">{{row[0]}}</text><text v-for="(value,j) in row.slice(1)" :key="j" :x="260+j*220" :y="98+i*60" class="shape">{{value}}</text></g>
 <g v-if="reveal>=2" data-reveal-step="2"><text x="30" y="231" class="mono">2×0.2 + (−1)×(−0.3) + 0.5×0.4 + bias 0.1 = 1.0</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="295" class="mono">ReLU(1.0) = max(0, 1.0) = 1.0</text><text x="30" y="349" class="small">A negative sum would become zero. Each hidden unit has its own learned weights.</text></g>
</g>
<g v-else-if="mode==='filter'">
 <text x="20" y="25" class="label">ONE TEMPORAL FILTER · TWO CHANNELS × FIVE POSITIONS</text>
 <text x="30" y="100">XRSA</text><text x="30" y="157">XRSB</text>
 <g v-for="i in 10" :key="i"><rect :x="150+(i-1)*61" y="70" width="48" height="39" fill="#bad8cd"/><rect :x="150+(i-1)*61" y="127" width="48" height="39" fill="#52776d"/></g>
 <rect :x="reveal>=3?211:150" y="60" width="292" height="116" fill="none" stroke="#c17b40" stroke-width="4"/>
 <g v-if="reveal>=2" data-reveal-step="2"><text x="30" y="237">Multiply by 10 learned weights, sum, then add one bias.</text><text x="30" y="278" class="mono">Conv1d(in_channels=2, out_channels=width, kernel_size=5)</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="340">Move one minute right; reuse the same weights.</text><text x="30" y="375" class="small">Padding of two keeps 60 positions. Each output channel learns a different filter.</text></g>
</g>
<g v-else-if="mode==='gradient'">
 <text x="20" y="25" class="label">ARITHMETIC EXAMPLE · PLAIN GRADIENT DESCENT, NOT THE WORKSHOP ADAM RUN</text>
 <text x="30" y="95" class="mono">x = 2     target = 3     weight w = 1</text>
 <text x="30" y="151" class="mono">prediction = w × x = 2     loss = (2 − 3)² = 1</text>
 <g v-if="reveal>=2" data-reveal-step="2"><text x="30" y="220" class="mono">d(loss)/dw = 2 × (prediction − target) × x = −4</text><text x="30" y="263" class="small">The negative slope says increasing this weight will lower the loss nearby.</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="327" class="mono">new w = 1 − 0.1 × (−4) = 1.4 → prediction 2.8</text><text x="30" y="372" class="small">Adam uses gradient history to set updates. The learning rate still controls their scale.</text></g>
</g>
<g v-else-if="mode==='image'">
 <text x="20" y="25" class="label">IMAGE BATCH · CHANNELS ARE TWO OBSERVATION TIMES</text>
 <g transform="translate(30 70)"><rect x="20" y="0" width="190" height="160" fill="#dbe6e1" stroke="#52776d"/><circle cx="115" cy="80" r="61" fill="#c17b40"/><text x="0" y="204" class="mono">x[:, 0:1] · −60 min</text></g>
 <g transform="translate(315 70)"><rect width="190" height="160" fill="#dbe6e1" stroke="#52776d"/><circle cx="95" cy="80" r="61" fill="#d99f50"/><text x="0" y="204" class="mono">x[:, 1:2] · now</text></g>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M530 150H630" class="arrow"/><text x="650" y="96">CNN correction</text><text x="650" y="151" class="shape">[B, 1, 64, 64]</text><text x="650" y="204" class="small">One value for each predicted pixel</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="332" class="mono">forecast = x[:, 1:2] + correction</text><text x="30" y="372" class="small">The slice 1:2 retains the channel axis. Both added arrays have the same shape.</text></g>
</g>
<g v-else-if="mode==='averaging'">
 <text x="20" y="25" class="label">PUBLIC SCORER FIXTURE · ILLUSTRATIVE PIXELS, NOT SATELLITE DATA</text>
 <g v-for="(values,k) in [[0,0,0,0,1,0,0,0,0],[0,0,0,0,2,2,0,2,2]]" :key="k" :transform="`translate(${50+k*350} 65)`"><rect v-for="(value,i) in values" :key="i" :x="i%3*55" :y="Math.floor(i/3)*55" width="50" height="50" :fill="value?'#f1ca70':'#dbe6e1'"/><text v-for="(value,i) in values" :key="'t'+i" :x="i%3*55+25" :y="Math.floor(i/3)*55+32" text-anchor="middle">{{value}}</text><text x="0" y="204" class="small">{{k===0?'1 included pixel · error sum 1':'4 included pixels · error sum 8'}}</text></g>
 <g v-if="reveal>=2" data-reveal-step="2"><text x="760" y="115" class="mono">Image 1: 1 / 1 = 1</text><text x="760" y="175" class="mono">Image 2: 8 / 4 = 2</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><text x="30" y="320" class="mono">Equal-image mean: (1 + 2) / 2 = 1.5</text><text x="30" y="367" class="small">Pooling all pixels gives 9 / 5 = 1.8. That is a different weighting rule.</text></g>
</g>
<g v-else-if="mode==='context'">
 <text x="20" y="25" class="label">WHAT EACH PROGRAM RECEIVES</text>
 <path d="M30 60H470V148H30Z" fill="#dbe6e1"/><text x="50" y="95">Research-agent request</text><text x="50" y="130" class="small">Source + settings + validation evidence</text>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M485 105H585" class="arrow"/><rect x="610" y="60" width="460" height="88" fill="#d8e5ec"/><text x="630" y="95">Reviewed training program</text><text x="630" y="130" class="small">Training inputs and training targets</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><path d="M830 160V215" class="arrow"/><rect x="610" y="232" width="460" height="92" fill="#f5dba0"/><text x="630" y="266">Fixed validation scorer</text><text x="630" y="303" class="small">Predictions compared with validation targets</text><path d="M595 275H240V162" class="arrow"/><text x="30" y="310" class="small">Return metrics and saved outputs.</text></g>
 <text x="30" y="375" class="small">Reserved-date predictions and scores enter only after model selection is frozen.</text>
</g>
<g v-else-if="mode==='selection'">
 <text x="20" y="25" class="label">TWO DECISIONS · PROPOSE CODE, THEN CHECK ITS MEASURED RESULT</text>
 <rect x="30" y="70" width="305" height="125" fill="#d8e5ec"/><text x="50" y="111">Agent composition</text><text x="50" y="148" class="small">Choose, combine,</text><text x="50" y="178" class="small">or retain source</text>
 <g v-if="reveal>=2" data-reveal-step="2"><path d="M350 130H420" class="arrow"/><rect x="440" y="70" width="245" height="125" fill="#f5dba0"/><text x="460" y="111">Train this source</text><text x="460" y="148" class="small">New weights</text><text x="460" y="178" class="small">and validation error</text></g>
 <g v-if="reveal>=3" data-reveal-step="3"><path d="M700 130H765" class="arrow"/><rect x="785" y="70" width="305" height="125" fill="#dbe6e1"/><text x="805" y="111">Notebook adoption</text><text x="805" y="151" class="small">Compare with the parent error</text><text x="30" y="260" class="mono">lower error → adopt</text><text x="30" y="300" class="mono">equal / worse / failed → retain</text><text x="30" y="340" class="small">A recommendation is not a trained version. The tested files determine what continues.</text></g>
</g>
</svg>
</template>
<style scoped>
.solar-concept{width:100%;height:385px;display:block;margin-top:12px}text{font:24px 'IBM Plex Sans',sans-serif;fill:#163c43}.small{font-size:19px}.mono{font:23px 'IBM Plex Mono',monospace}.shape{font:32px 'IBM Plex Mono',monospace}.label{font:14px 'IBM Plex Mono',monospace;fill:#52776d;letter-spacing:.6px}.axis,.arrow{fill:none;stroke:#52776d;stroke-width:2.5}.arrow{marker-end:var(--arrow)}
</style>
