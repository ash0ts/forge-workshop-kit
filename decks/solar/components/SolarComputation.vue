<script setup>
import {useId} from 'vue'
const props=defineProps({mode:{default:'normalization'}, reveal:{type:Number,default:99}})
const marker=useId().replace(/:/g,'')
const descriptions={
 normalization:'Log-transform both GOES channels. Fit one mean and standard deviation per channel using training inputs only. Reuse these values for every split. The target and persistence forecast remain unstandardized log10 XRS-B flux.',
 error:'Arithmetic example, not observed results: latest log-flux values minus their future targets give absolute errors 0.3, 0.1 and 0.0. Their mean absolute error is 0.133 log-flux units.',
 mlp:'The actual GOES MLP flattens two channels of sixty samples into 120 inputs, applies a learned linear layer of width 16 or 32, ReLU, then a final linear layer returning one log-flux forecast.',
 cnn:'The actual temporal CNN applies five-sample filters to both channels at each time position, with padding two. Its 16 or 32 channels are averaged over sixty time positions, then a linear layer produces one log-flux forecast.',
 training:'A training batch produces predictions and squared loss. Backpropagation computes gradients and Adam changes the forecasting model weights. Validation predicts without updating weights; its targets are scored in the parent process.',
 inference:'Final evaluation loads the saved model source and trained weights, predicts reserved-date inputs under eval and no_grad, then scores predictions against reserved targets. It does not call fit or take an optimizer step.',
 records:'One execution saves candidate.py, its configuration and dataset identity, weights.pt, predictions.npy and losses.json. W&B runs show metrics and settings; versioned Artifacts retain files; Agent Lens records the training operation.',
 checkpoint:'The completed local execution records and output files are uploaded as a checkpoint Artifact. After a new runtime restores and verifies the files, the journal is committed and the completed result is reused. An upload failure retries publication, not training.',
 evidence:'Current source, active configuration, validation results and a prior lesson enter the fixed research model. The final-test score is excluded. The model returns two code proposals and rationales. Each actual diff must be reviewed before it can train.',
 loss:'Arithmetic example: a prediction of 0.5 against target 1 gives signed error -0.5, squared loss 0.25 and absolute error 0.5. Training uses loss gradients; evaluation reports fixed absolute error. Changing the loss cannot change the evaluation rule.'
}
const samples=Array.from({length:60},(_,i)=>i)
</script>
<template><svg viewBox="0 0 1120 390" role="img" :aria-label="descriptions[mode]" :style="{'--arrow':`url(#${marker})`}">
<defs><marker :id="marker" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6" fill="none" stroke="#52776d" stroke-width="1.7"/></marker></defs>
<g v-if="mode==='normalization'">
 <text x="25" y="28" class="label">INPUTS · XRSA AND XRSB</text>
 <text x="25" y="72" class="mono">flux in W/m²</text><path d="M170 64H220" class="arrow"/><text x="240" y="72" class="mono">log10(flux)</text>
<g v-if="reveal>=2" data-reveal-step="2"> <path d="M390 64H450" class="arrow"/>
 <rect x="470" y="38" width="620" height="71" fill="#bad8cd" rx="3"/><text x="490" y="68">Fit each channel’s mean μ and standard deviation σ</text><text x="490" y="94" class="small">Training dates only · February 1–10 · x = (log10(flux) − μ) / σ</text>
 <path d="M780 110V147" class="arrow"/></g>
<g v-if="reveal>=3" data-reveal-step="3"> <g v-for="(label,i) in ['Training','Validation','Final test']" :key="label" :transform="`translate(${25+i*365} 166)`"><rect width="335" height="82" :fill="['#dbe6e1','#f5dba0','#d8e5ec'][i]"/><text x="167" y="29" text-anchor="middle">{{label}}</text><text x="167" y="61" text-anchor="middle" class="small">Apply the same saved μ and σ</text></g>
 <path d="M780 149H192V159M780 149H557V159M780 149H922V159" class="line"/></g>
<g v-if="reveal>=4" data-reveal-step="4"> <line x1="25" y1="281" x2="1090" y2="281" class="divider"/>
 <text x="25" y="316" class="label">TARGET + PERSISTENCE</text><text x="330" y="317" class="mono">log10(XRS-B)</text><text x="590" y="317">Keep these in log-flux units.</text>
 <text x="25" y="363" class="small">Copy split["persistence"], not the standardized input tensor, for the baseline.</text></g>
</g>
<g v-else-if="mode==='error'">
 <text x="25" y="24" class="label">ARITHMETIC EXAMPLE · VALUES ARE NOT WORKSHOP RESULTS</text>
 <text x="215" y="68" text-anchor="middle">Latest reading</text><text x="490" y="68" text-anchor="middle">Future target</text><text x="800" y="68" text-anchor="middle">Absolute error</text>
 <g v-for="(r,i) in [['−6.0','−5.7','0.3'],['−5.5','−5.6','0.1'],['−6.2','−6.2','0.0']]" :key="i" :transform="`translate(0 ${96+i*61})`"><rect x="100" width="230" height="44" fill="#dbe6e1" rx="3"/><text x="215" y="29" text-anchor="middle" class="mono">{{r[0]}}</text><text x="365" y="29">−</text><text x="490" y="29" text-anchor="middle" class="mono">{{r[1]}}</text><path d="M580 21H670" class="arrow"/><text x="800" y="29" text-anchor="middle" class="mono">| {{r[0]}} − ({{r[1]}}) | = {{r[2]}}</text></g>
 <path d="M972 94H995V261H972" class="line"/><path d="M995 270V300H735" class="arrow"/>
 <text x="25" y="330">Persistence uses the latest reading as its prediction.</text>
 <text x="735" y="330" class="mono">(0.3 + 0.1 + 0) / 3 = 0.133</text>
 <text x="25" y="372" class="small">A 0.3 log10 error is about a 2× flux ratio. The sign is removed before averaging.</text>
</g>
<g v-else-if="mode==='mlp'||mode==='cnn'">
 <text x="25" y="25" class="label">GOES INPUT · BATCH AXIS OMITTED</text>
 <text x="25" y="79">XRSA</text><text x="25" y="116">XRSB</text>
 <g v-for="i in samples" :key="i"><rect :x="112+i*4" y="58" width="3" height="27" :fill="mode==='cnn'&&i>=22&&i<27?'#b57339':'#8fb2a4'"/><rect :x="112+i*4" y="95" width="3" height="27" :fill="mode==='cnn'&&i>=22&&i<27?'#b57339':'#52776d'"/></g>
 <text x="112" y="155" class="small">60 time samples →</text><text x="112" y="182" class="mono">shape: [2, 60]</text>
 <g v-if="mode==='mlp'">
<g v-if="reveal>=2" data-reveal-step="2">  <path d="M365 90H435" class="arrow"/><text x="495" y="49" text-anchor="middle">Flatten</text>
  <g v-for="i in 12" :key="i"><rect :x="447+(i-1)%4*22" :y="65+Math.floor((i-1)/4)*22" width="16" height="16" :fill="i<7?'#8fb2a4':'#52776d'"/></g><text x="490" y="161" text-anchor="middle" class="small">120 values</text></g>
<g v-if="reveal>=3" data-reveal-step="3">  <g v-for="i in 5" :key="i"><line x1="543" :y1="72+(i-1)*12" x2="650" :y2="56+(i-1)*24" stroke="#aabbb2"/><circle cx="660" :cy="56+(i-1)*24" r="8" fill="#163c43"/></g>
  <text x="660" y="201" text-anchor="middle">Linear → ReLU</text><text x="660" y="231" text-anchor="middle" class="small">width 16 or 32</text></g>
<g v-if="reveal>=4" data-reveal-step="4">  <path d="M685 105H880" class="arrow"/><circle cx="910" cy="105" r="18" fill="#f1ca70"/><text x="910" y="158" text-anchor="middle">Linear → 1 value</text><text x="910" y="189" text-anchor="middle" class="small">Future log XRS-B</text>
  <text x="25" y="298">Each hidden unit learns a weight for every channel and time position.</text>
  <text x="25" y="355" class="mono">Flatten → Linear(120, width) → ReLU → Linear(width, 1)</text></g>
 </g>
 <g v-else>
<g v-if="reveal>=2" data-reveal-step="2">  <rect x="197" y="49" width="27" height="82" fill="none" stroke="#b57339" stroke-width="3"/><path d="M365 90H420" class="arrow"/>
  <text x="127" y="232" class="small">5-sample filter</text><text x="127" y="260" class="small">slides across time</text>
  <g v-for="i in 4" :key="i"><rect x="438" :y="55+(i-1)*29" width="218" height="20" :fill="i%2?'#bad8cd':'#52776d'"/></g>
  <text x="545" y="201" text-anchor="middle" class="small">width channels × 60</text><text x="545" y="230" text-anchor="middle" class="small">padding = 2 · ReLU</text></g>
<g v-if="reveal>=3" data-reveal-step="3">  <path d="M670 105H730" class="arrow"/><text x="800" y="82" text-anchor="middle">Average over time</text><text x="800" y="119" text-anchor="middle" class="mono">[width, 1]</text></g><g v-if="reveal>=4" data-reveal-step="4"><path d="M890 105H947" class="arrow"/><circle cx="985" cy="105" r="18" fill="#f1ca70"/><text x="985" y="161" text-anchor="middle">Linear → 1</text>
  <text x="25" y="310">The same filter weights are reused at every time position.</text>
  <text x="25" y="359" class="mono">Conv1d(2, width, 5, padding=2) → ReLU → AvgPool → Linear</text></g>
 </g>
</g>
<g v-else-if="mode==='training'">
 <text x="25" y="27" class="label">GOES TRAINING · REPEAT FOR EACH OPTIMIZER STEP</text>
 <text x="25" y="87">Training inputs</text><path d="M190 79H260" class="arrow"/><g transform="translate(280 44)"><rect width="180" height="87" fill="#163c43" rx="4"/><text x="90" y="34" text-anchor="middle" class="white">Forecast model</text><text x="90" y="65" text-anchor="middle" class="small white">current weights</text></g>
 <path d="M475 79H540" class="arrow"/><text x="565" y="87">Predictions</text><g v-if="reveal>=2" data-reveal-step="2"><path d="M692 79H755" class="arrow"/><text x="830" y="69" text-anchor="middle">Squared training loss</text><text x="830" y="105" text-anchor="middle" class="mono">prediction vs target</text>
 <text x="830" y="182" text-anchor="middle">Training targets</text><path d="M830 153V122" class="arrow"/></g>
<g v-if="reveal>=3" data-reveal-step="3"> <path d="M1000 80H1075V258H470" class="arrow"/><text x="790" y="242" text-anchor="middle" class="mono">loss.backward() → optimizer.step()</text>
 <path d="M445 258H370V145" class="arrow"/><text x="370" y="298" text-anchor="middle">Adam updates these weights</text></g>
<g v-if="reveal>=4" data-reveal-step="4"> <text x="25" y="368" class="small">Validation runs model.eval() with no_grad(); its targets are scored outside candidate code.</text></g>
</g>
<g v-else-if="mode==='inference'">
 <text x="25" y="27" class="label">FINAL EVALUATION · NO FIT CALL OR OPTIMIZER STEP</text>
 <path d="M25 58H290L315 83V158H25Z" fill="#e7e3d7" stroke="#9bad9e"/><text x="45" y="98" class="mono">candidate.py + config</text><text x="45" y="134" class="small">The selected model structure</text>
 <g v-for="i in 12" :key="i"><rect :x="40+(i-1)%4*19" :y="211+Math.floor((i-1)/4)*19" width="15" height="15" :fill="i%3?'#52776d':'#bad8cd'"/></g><text x="140" y="236" class="mono">weights.pt</text><text x="140" y="269" class="small">Learned parameters</text>
<g v-if="reveal>=2" data-reveal-step="2"> <path d="M330 106H430M330 244H430" class="arrow"/>
 <rect x="449" y="68" width="300" height="223" rx="4" fill="#dbe6e1"/><text x="470" y="106" class="mono">model = build_model(...)</text><text x="470" y="151" class="mono">load_state_dict(weights)</text><text x="470" y="195" class="mono">model.eval()</text><text x="470" y="239" class="mono">torch.no_grad()</text><text x="470" y="271" class="small">predict reserved inputs</text>
 <text x="600" y="342" text-anchor="middle">Reserved-date inputs</text><path d="M600 314V301" class="arrow"/></g>
<g v-if="reveal>=3" data-reveal-step="3"> <path d="M762 167H825" class="arrow"/><text x="842" y="175">Predictions</text><path d="M920 186V246" class="arrow"/></g>
<g v-if="reveal>=4" data-reveal-step="4"> <text x="1090" y="235" text-anchor="end" class="small">Future targets</text><path d="M1050 244V264" class="arrow"/>
 <rect x="840" y="269" width="250" height="62" fill="#f1ca70" rx="4"/><text x="965" y="306" text-anchor="middle">Fixed scorer</text>
 <text x="25" y="382" class="small">Source and weights are separate inputs. Reserved targets enter only the scorer.</text></g>
</g>
<g v-else-if="mode==='records'">
 <path d="M25 45H180L205 70V218H25Z" fill="#e7e3d7" stroke="#9bad9e"/><text x="45" y="89" class="mono">candidate.py</text><text x="45" y="129" class="small">config + seed</text><text x="45" y="164" class="small">dataset version</text><text x="45" y="199" class="small">train/validation</text>
 <path d="M225 133H305" class="arrow"/><text x="395" y="124" text-anchor="middle">run_training(...)</text><text x="395" y="158" text-anchor="middle" class="small">one saved execution</text>
 <path d="M500 133H565" class="arrow"/>
 <path d="M584 44V279H875" class="line"/>
 <g v-for="(f,i) in ['candidate.py · executed source','weights.pt · learned parameters','predictions.npy · model outputs','losses.json · training history']" :key="f"><path :d="`M584 ${70+i*57}H610`" class="line"/><text x="624" :y="77+i*57" class="mono">{{f}}</text></g>
 <text x="25" y="326">W&B run: settings + scores</text><text x="600" y="326">Artifact: versioned output files</text>
 <text x="25" y="371" class="small">Agent Lens links the train_and_validate operation to the same execution and its returned metrics.</text>
</g>
<g v-else-if="mode==='checkpoint'">
 <text x="25" y="26" class="label">AFTER AN EXECUTION HAS COMPLETED</text>
 <rect x="28" y="66" width="290" height="190" rx="8" fill="none" stroke="#52776d" stroke-width="3"/><line x1="28" y1="218" x2="318" y2="218" class="line"/><text x="173" y="109" text-anchor="middle">Notebook runtime</text><text x="53" y="153" class="mono">journal.json</text><text x="53" y="185" class="mono">outputs / files</text>
 <path d="M335 150H463" class="arrow"/><text x="399" y="123" text-anchor="middle" class="small">checkpoint()</text>
 <path d="M490 91L595 56L700 91V219L595 254L490 219Z" fill="#dbe6e1" stroke="#52776d" stroke-width="2"/><text x="595" y="143" text-anchor="middle">Checkpoint</text><text x="595" y="176" text-anchor="middle">Artifact version</text>
 <path d="M720 150H825" class="arrow"/><text x="772" y="123" text-anchor="middle" class="small">restore()</text>
 <rect x="842" y="66" width="250" height="190" rx="8" fill="none" stroke="#52776d" stroke-width="3"/><text x="967" y="108" text-anchor="middle">New runtime</text><text x="864" y="148" class="small">1. Verify output files</text><text x="864" y="181" class="small">2. Restore journal</text><text x="864" y="214" class="small">3. Show saved result</text>
 <text x="25" y="320">If upload fails, keep the local result and retry publication.</text>
 <text x="25" y="367" class="small">Restoring a completed stage does not train the model or resend its inference request.</text>
</g>
<g v-else-if="mode==='evidence'">
 <path d="M25 45H300L325 70V280H25Z" fill="#e7e3d7" stroke="#9bad9e"/><text x="48" y="88" class="mono">candidate.py</text><text x="48" y="128">Active settings</text><text x="48" y="168">Validation errors + losses</text><text x="48" y="208">Failed attempts + lesson</text><text x="48" y="253" class="small">select_validation_evidence(...)</text>
 <path d="M340 159H420" class="arrow"/><rect x="440" y="94" width="220" height="130" rx="6" fill="#163c43"/><text x="550" y="135" text-anchor="middle" class="white">Research agent</text><text x="550" y="174" text-anchor="middle" class="small white">Fixed language model</text><text x="550" y="203" text-anchor="middle" class="small white">reads → proposes</text>
 <path d="M675 159C715 159 708 84 752 84M675 159C715 159 708 253 752 253" class="arrow"/>
 <g v-for="(letter,i) in ['A','B']" :key="letter" :transform="`translate(770 ${35+i*169})`"><path d="M0 0H285V112H0Z" fill="#f9f6ec" stroke="#9bad9e"/><text x="18" y="28">Candidate {{letter}} · review diff</text><text x="18" y="58" class="mono deletion">− previous implementation</text><text x="18" y="86" class="mono addition">+ proposed implementation</text></g>
 <text x="25" y="327" class="small">Final-test records are rejected before this request.</text><text x="770" y="352" class="small">You review each diff before training.</text>
 <text x="25" y="376" class="label">WORKFLOW DIAGRAM · THE NEXT SLIDES SHOW THE RECORDED CHANGES</text>
</g>
<g v-else-if="mode==='loss'">
 <text x="25" y="26" class="label">ARITHMETIC EXAMPLE · ONE PIXEL INSIDE THE MASK</text>
 <text x="40" y="94">Prediction = 0.5</text><text x="40" y="134">Target = 1.0</text><path d="M240 110H320" class="arrow"/><text x="345" y="113" class="mono">error = −0.5</text>
<g v-if="reveal>=2" data-reveal-step="2"> <path d="M535 110C600 110 590 68 660 68M535 110C600 110 590 232 660 232" class="arrow"/>
 <text x="690" y="75" class="mono">square(−0.5) = 0.25</text><text x="690" y="113" class="small">Starting training loss</text><text x="690" y="146" class="small">Its gradient updates weights</text></g>
<g v-if="reveal>=3" data-reveal-step="3"> <text x="690" y="238" class="mono">abs(−0.5) = 0.5</text><text x="690" y="276" class="small">Fixed evaluation error</text><text x="690" y="309" class="small">Used to compare every candidate</text>
 <text x="25" y="366" class="small">The agent can change the training loss. It cannot change how evaluation error is calculated.</text></g>
</g>
</svg></template>
<style scoped>
svg{display:block;width:100%;height:390px;margin-top:12px}text{font:23px 'IBM Plex Sans',Arial;fill:#163c43}.small{font-size:19px}.label{font:14px 'IBM Plex Mono',monospace;letter-spacing:1px;fill:#52776d}.mono{font:19px 'IBM Plex Mono',monospace}.white{fill:#f6f2e7}.line,.arrow{fill:none;stroke:#52776d;stroke-width:2}.arrow{marker-end:var(--arrow)}.divider{stroke:#bac7bd;stroke-width:1}.deletion{fill:#9c593c;font-size:16px}.addition{fill:#28715b;font-size:16px}
</style>
