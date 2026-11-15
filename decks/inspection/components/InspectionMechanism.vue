<script setup>
import {computed,ref} from 'vue'
import fact from '../data/feature-example.json'
const asset=(name)=>`${import.meta.env.BASE_URL}images/${name}`
const props=defineProps({kind:String,step:{type:Number,default:1},caseId:{type:String,default:'pcb1-anomaly-048'}})
const threshold=ref(.7)
const fixture=[{score:.95,defect:false},{score:.9,defect:true},{score:.7,defect:true},{score:.4,defect:true},{score:.1,defect:false}]
const misses=computed(()=>fixture.filter(r=>r.defect&&r.score<threshold.value).length)
const alarms=computed(()=>fixture.filter(r=>!r.defect&&r.score>=threshold.value).length)
const outcome=computed(()=>fact.outcomes.filter(r=>r.case_id===props.caseId&&['whole','nearest-patch'].includes(r.version)))
const image=computed(()=>props.caseId.endsWith('048')?'case-corrected':'case-regression')
const code={data:['photo = record["image"]','label = record["label"]','mask = record["mask"]','# The photograph becomes model input.','# The label is its training target.','# The mask is only for inspection.'],encoder:['image.shape == (3, 224, 224)','whole.shape == (N, 512)','patches.shape == (N, 14, 14, 64)','# ResNet-18 weights stay fixed.'],patch:['scale = maximum(bank.std(axis=0), .1)','difference = query/scale - bank/scale','squared = mean(difference**2, axis=-1)','distance = min(squared)','# Match only the same spatial position.','# A training board cannot match itself.'],features:['errors = nearest_patch_errors(data, rows, bank)','local = log1p(errors).reshape(len(rows), -1)','X = concatenate([whole, local], axis=1)','# 512 + 196 = 708 columns per board.'],threshold:['positive_scores = sort(scores[y == 1])[::-1]','position = ceil(recall * len(positive_scores)) - 1','threshold = positive_scores[position]','flagged = scores >= threshold'],ranking:['# At each newly retrieved defect:','precision = true_positives / retrieved','AP = mean([1/2, 2/3, 3/4])','# AP = 0.638889 for this public fixture.'],review:['distance = abs(scores - threshold)','active = rows[argsort(distance)[:24]]','random = rng.choice(rows, 24, replace=False)','# Both start from the same detector.','# Reveal labels after selection.'],train:['model = inspection.fit_classifier(','    data, fit_rows, method,','    build_features=build_features, C=.03',')','scores = inspection.score(','    data, validation_rows, model,','    build_features=build_features',')'],freeze:['save(reference_bank, normalization)','save(feature_source, classifier, threshold)','# Reload exactly these files.','predict(the_same_case_ids)'],outcomes:['predicted_defect = score >= saved_threshold','# Compare each detector with its own cutoff.','# The photograph and label stay the same.']}
</script>
<template>
<div class="im-layout"><div class="im-visual">
<svg v-if="kind==='data'" viewBox="0 0 660 440" role="img" :aria-label="step>1?'Actual VisA board photograph and supplied defect mask. Only the photograph enters the classifier; the mask is for human inspection.':'A VisA PCB1 fitting photograph. Decide whether this board should pass before seeing its label and annotation.'">
 <text x="12" y="29" class="heading">{{step>1?`${fact.case_id} · actual fitting example`:'VisA PCB1 fitting example'}}</text>
 <image :href="asset('fit-defect-image.jpg')" x="12" y="55" width="270" height="245" preserveAspectRatio="xMidYMid meet"/>
 <g v-if="step>1"><image class="im-mask" :href="asset('fit-defect-mask.png')" x="370" y="55" width="270" height="245" preserveAspectRatio="xMidYMid meet"/><text x="386" y="329" class="small">Supplied defect annotation</text></g>
 <text x="15" y="329" class="small">Photograph → model input</text><path d="M148 344V380H300" class="arrow"/><text x="310" y="388" class="heading">Predict defective / normal</text>
 <path v-if="step>1" d="M495 344V369M484 345L506 367M506 345L484 367" class="orange-line"/>
 <text x="12" y="430" class="small">{{step>1?'White mask pixels locate the annotation. No mask enters this detector.':'Would you pass this board or send it for inspection?'}}</text>
</svg>
<svg v-else-if="kind==='encoder'" viewBox="0 0 660 440" role="img" aria-label="A 224 by 224 RGB photo goes through frozen ResNet-18. Whole-image features have 512 channels; local features retain 14 by 14 spatial positions and 64 channels per position.">
 <image :href="asset('fit-defect-image.jpg')" x="12" y="50" width="185" height="185"/>
 <text x="12" y="28" class="heading">224 × 224 × 3</text><path d="M208 144H252" class="arrow"/>
 <rect x="265" y="81" width="130" height="125" class="teal"/><text x="280" y="127" class="heading">ResNet-18</text><text x="282" y="159" class="small">frozen</text><path d="M407 144H447" class="arrow"/>
 <g v-for="i in 14" :key="i"><rect :x="466+i%7*24" :y="92+Math.floor(i/7)*43" width="17" height="35" class="blue"/></g><text x="455" y="235" class="small">512 whole-image values</text>
 <g v-if="step>1"><path d="M330 220V276H178" class="arrow"/>
 <rect v-for="i in 196" :key="i" :x="16+i%14*11" :y="268+Math.floor(i/14)*9" width="9" height="7" :class="i===105?'orange':'teal'"/>
 <text x="214" y="311" class="heading">14 × 14 × 64</text><text x="214" y="344" class="small">196 locations, each with a 64-value vector</text><text x="214" y="377" class="small">Keep spatial differences instead of pooling them away.</text></g>
 <text x="12" y="431" class="small">Schematic features; nearby locations have overlapping receptive fields.</text>
</svg>
<svg v-else-if="kind==='patch'" viewBox="0 0 660 440" role="img" aria-label="At spatial position 7,7, the actual defect-board vector is compared with 361 normal training vectors. The closest normal is selected; displayed distances are computed from saved feature values.">
 <text x="12" y="28" class="heading">One query position: row 7, column 7</text>
 <image :href="asset('fit-defect-image.jpg')" x="12" y="65" width="180" height="180"/>
 <rect x="102" y="155" width="13" height="13" class="patch-marker"/>
 <path d="M202 162H238" class="arrow"/>
 <text x="254" y="72" class="small">Normal training bank · {{fact.normal_bank_size}} boards</text>
 <g v-for="(item,i) in fact.distances" :key="item.case_id">
  <text x="252" :y="110+i*54" class="small">{{item.case_id.replace('pcb1-','')}}</text>
  <rect x="425" :y="91+i*54" :width="item.distance*100" height="24" :class="item.closest?'teal':'pale'"/>
  <text :x="433+item.distance*100" :y="110+i*54" class="small">{{item.distance.toFixed(3)}}</text>
 </g>
 <text x="12" y="326" class="heading">Minimum distance = {{fact.closest_distance.toFixed(3)}}</text>
 <text x="12" y="364" class="small">Scaled mean squared difference across 64 channels.</text>
 <text x="12" y="399" class="small">Four bank rows shown; the minimum searches all {{fact.normal_bank_size}}.</text>
 <text x="12" y="432" class="small">Repeat at all 196 positions. Exclude a training board’s own match.</text>
</svg>
<svg v-else-if="kind==='features'" viewBox="0 0 660 440" role="img" aria-label="The 14 by 14 nearest-patch distance grid is transformed by log1p, flattened into 196 numbers and appended to 512 whole-image features to create 708 columns for each board.">
 <text x="12" y="28" class="heading">Preserve one row per board</text>
 <g v-for="i in 196" :key="i"><rect :x="12+i%14*11" :y="68+Math.floor(i/14)*10" width="9" height="8" :class="i===105?'orange':'pale'"/></g>
 <path d="M176 140H220" class="arrow"/><text x="231" y="120" class="heading">log1p</text><text x="231" y="155" class="small">{{fact.closest_distance.toFixed(3)}} → {{fact.log1p_closest_distance.toFixed(3)}}</text>
 <path d="M384 140H430" class="arrow"/>
 <g v-for="i in 14" :key="i"><rect :x="446+i%7*24" :y="92+Math.floor(i/7)*36" width="20" height="27" :class="i===6?'orange':'teal'"/></g><text x="444" y="214" class="small">196 local values</text>
 <rect x="13" y="268" width="450" height="52" class="blue"/><rect x="463" y="268" width="173" height="52" class="teal"/><text x="28" y="300" class="small">512 whole-image values</text><text x="473" y="300" class="small">196 local</text>
 <path d="M12 337V354H636V337" class="arrow"/><text x="182" y="392" class="heading">708 classifier inputs</text>
 <text x="12" y="432" class="small">The grid is schematic; the highlighted calculation uses actual cached values.</text>
</svg>
<template v-else-if="kind==='threshold'">
 <svg viewBox="0 0 660 340" role="img" aria-label="The public five-board check separates defects and normal boards on a score axis. Moving the cutoff changes missed defects and false alarms without changing scores.">
 <text x="12" y="28" class="heading">Public check: three defects, two normal boards</text>
 <text x="12" y="93" class="small">Defects</text><text x="12" y="183" class="small">Normal</text>
 <rect :x="145+threshold*475" y="57" :width="(1-threshold)*475" height="150" class="pale"/>
 <path d="M145 98H620M145 188H620M145 220H620" class="arrow"/>
 <g v-for="(r,i) in fixture" :key="i"><circle :cx="145+r.score*475" :cy="r.defect?98:188" r="12" :class="r.defect?'teal':'paper'"/><text :x="145+r.score*475" :y="r.defect?72:164" text-anchor="middle" class="small">{{r.score}}</text></g>
 <path :d="`M${145+threshold*475} 52V232`" class="orange-line"/>
 <text x="143" y="253" class="small">0</text><text x="608" y="253" class="small">1</text><text x="143" y="296" class="heading">{{misses}} missed defects · {{alarms}} false alarms</text>
 <text x="12" y="331" class="small">Flag every score at or above the cutoff; pale region is flagged.</text>
 </svg>
 <label class="im-slider">Cutoff {{threshold.toFixed(2)}}<input aria-label="Five-board inspection cutoff" type="range" min="0" max="1" step=".05" v-model.number="threshold"/></label>
 <p class="im-caption">{{step===1?'At .70, detect 2 of 3 defects: recall ⅔.':'For the actual validation set, ceil(.90 × 12) = 11 defects must be caught.'}}</p>
</template>
<svg v-else-if="kind==='ranking'" viewBox="0 0 660 440" role="img" aria-label="The five public fixture scores produce precision 1/2, 2/3, and 3/4 at successive defect retrievals. The three equal recall increments yield average precision 0.639.">
 <text x="12" y="28" class="heading">Same fixture, sorted by defect score</text>
 <g v-for="(r,i) in fixture" :key="i"><rect :x="15+i*127" y="49" width="108" height="49" :class="r.defect?'teal':'paper'"/><text :x="69+i*127" y="79" text-anchor="middle" class="small">{{r.defect?'defect':'normal'}} {{r.score}}</text><text :x="69+i*127" y="124" text-anchor="middle" class="small">rank {{i+1}}</text></g>
 <path d="M68 166V362H550" class="arrow"/><text x="12" y="165" class="small">precision</text><text x="577" y="393" class="small">recall</text>
 <rect x="70" y="266" width="160" height="96" class="pale"/><rect x="230" y="234" width="160" height="128" class="pale"/><rect x="390" y="218" width="160" height="144" class="pale"/>
 <path d="M70 266H230V234H390V218H550" class="teal-line"/>
 <text x="117" y="252" class="small">1 / 2</text><text x="278" y="220" class="small">2 / 3</text><text x="438" y="204" class="small">3 / 4</text>
 <text x="208" y="389" class="small">⅓</text><text x="370" y="389" class="small">⅔</text><text x="539" y="389" class="small">1</text>
 <text x="12" y="432" class="small">AP = (½ + ⅔ + ¾) / 3 = .639 · fixture calculation, not the PCB1 result</text>
</svg>
<svg v-else-if="kind==='review'" viewBox="0 0 660 440" role="img" aria-label="Two 24-label acquisitions share the same 133-board review pool. Uncertainty sampling selects near the current cutoff, random sampling spans the pool. Both train with 397 plus 24 rows.">
 <text x="12" y="28" class="heading">Same parent detector · same 133-board pool</text>
 <text x="12" y="74" class="small">Near the cutoff</text><text x="12" y="205" class="small">Random, seed 17</text>
 <g v-for="lane in [0,1]" :key="lane">
  <path :d="`M15 ${140+lane*131}H631`" class="arrow"/>
  <circle v-for="i in 32" :key="i" :cx="25+(i-1)*19" :cy="115+lane*131" r="6" :class="lane===0?(i>=13&&i<=20?'orange':'pale'):([2,6,9,14,18,23,27,31].includes(i)?'blue':'pale')"/>
  <path :d="`M320 ${88+lane*131}V${153+lane*131}`" class="orange-line"/>
 </g>
 <text x="334" y="176" class="small">current cutoff</text>
 <path d="M178 290V312H480V290M328 312V340" class="arrow"/>
 <text x="94" y="377" class="heading">Each branch fits on 397 + 24 boards</text>
 <text x="12" y="401" class="small">Schematic score positions; select 24 labels in each actual branch.</text>
 <text x="12" y="430" class="small">More labels can help either branch. Compare the selection rules fairly.</text>
</svg>
<svg v-else-if="kind==='train'" viewBox="0 0 660 440" role="img" aria-label="397 training feature rows and their labels fit classifier weights. A separate 132-row validation matrix uses the fixed weights to produce scores. The same learner-authored feature function supplies both matrices.">
 <text x="12" y="28" class="heading">Training learns the classifier weights</text>
 <g v-for="i in 48" :key="i"><rect :x="12+i%8*18" :y="70+Math.floor(i/8)*15" width="14" height="11" :class="i%3?'blue':'pale'"/></g>
 <g v-for="i in 6" :key="i"><circle cx="174" :cy="75+(i-1)*15" r="6" :class="i%2?'teal':'orange'"/></g>
 <text x="12" y="190" class="small">397 feature rows + labels</text><path d="M204 116H278" class="arrow"/><text x="226" y="99" class="small">fit</text>
 <g v-for="i in 8" :key="i"><rect :x="301+(i-1)*27" y="86" width="20" :height="30+(i%3)*13" :class="i%2?'teal':'orange'"/></g><text x="300" y="190" class="small">Learned coefficients + intercept</text>
 <g :opacity="step>1?1:.25"><path d="M420 202V246" class="arrow"/><text x="445" y="231" class="small">weights stay fixed</text>
 <g v-for="i in 32" :key="i"><rect :x="12+i%8*18" :y="261+Math.floor(i/8)*15" width="14" height="11" class="pale"/></g>
 <path d="M170 291H278" class="arrow"/><text x="183" y="272" class="small">score</text><rect x="300" y="260" width="245" height="64" class="paper"/><text x="321" y="300" class="heading">Apply saved classifier</text>
 <text x="12" y="353" class="small">132 validation rows</text><text x="301" y="353" class="small">132 scores → choose cutoff</text></g>
 <text x="12" y="400" class="small">Both matrices use your build_features function.</text><text x="12" y="430" class="small">Schematic cells and coefficients; recorded partition sizes.</text>
</svg>
<svg v-else-if="kind==='freeze'" viewBox="0 0 660 440" role="img" aria-label="Training uses 397 fitting rows and changes classifier weights. Validation applies the same feature function to 132 different boards without fitting. A release preserves the reference bank, feature source, weights and threshold together.">
 <text x="12" y="28" class="heading">{{kind==='train'?'Fit once; score different boards':'Save every part needed to reproduce a score'}}</text>
 <g v-for="(n,i) in ['Reference bank','Feature source','Classifier weights','Cutoff']" :key="n"><path :d="`M${15+i*160} 69h144v110h-144z`" class="paper"/><path :d="`M${31+i*160} 94h105M${31+i*160} 115h105M${31+i*160} 136h75`" class="arrow"/><text :x="17+i*160" y="208" class="small">{{n}}</text></g>
 <path d="M90 224V250H560V224M330 250V286" class="arrow"/>
 <rect x="126" y="291" width="405" height="54" class="teal"/><text x="147" y="325" class="heading">Same feature implementation</text>
 <path d="M330 351V377H110M330 377H550" class="arrow"/><text x="14" y="414" class="small">397 fitting boards → weights</text><text x="350" y="414" class="small">132 validation boards → scores</text>
</svg>
<svg v-else-if="kind==='outcomes'" viewBox="0 0 660 440" role="img" :aria-label="`Actual ${caseId} photograph and mask with the saved whole-image and nearest-patch predictions and their frozen thresholds.`">
 <text x="12" y="29" class="heading">{{caseId}} · recorded teaching retest</text>
 <image :href="asset(`${image}-image.jpg`)" x="12" y="53" width="285" height="236"/><image class="im-mask" :href="asset(`${image}-mask.png`)" x="345" y="53" width="285" height="236"/>
 <text x="12" y="310" class="small">Actual photograph</text><text x="346" y="310" class="small">Supplied defect mask</text>
 <g v-for="(r,i) in outcome" :key="r.version"><rect x="12" :y="329+i*50" width="622" height="42" :class="r.score>=r.threshold?'teal':'orange'"/><text x="26" :y="357+i*50" class="small">{{r.version}}: score {{r.score.toFixed(3)}} ≥ cutoff {{r.threshold.toFixed(3)}}? {{r.score>=r.threshold?'Yes: defect caught':'No: defect missed'}}</text></g>
</svg>
</div><div class="im-code"><div class="im-label">Code behind the figure</div><pre><span v-for="(line,i) in code[kind]" :key="i" :class="{active:i===Math.min(step-1,code[kind].length-1)}">{{line}}</span></pre><p class="im-caption">{{kind==='patch'?'Distances derived from the actual feature cache. Validation and test boards never join the reference bank.':kind==='outcomes'?'Both versions see the same board. A gain in the average does not remove every miss.':'The learner edits this operation in the notebook. This diagram runs no training.'}}</p></div></div>
</template>
<style scoped>
.im-mask{filter:brightness(255)}.im-layout{display:grid;grid-template-columns:1.45fr 1fr;gap:26px;align-items:start}.im-visual{min-width:0}.im-visual svg{display:block;width:100%;height:auto}.im-visual text{font:22px 'IBM Plex Sans';fill:#163c43}.im-visual .heading{font-size:24px;font-weight:500}.im-visual .small{font-size:18px}.teal{fill:#6aaa97}.blue{fill:#85b0c8}.orange{fill:#d9a16f}.pale{fill:#e0e6d9}.paper{fill:#fffaf0;stroke:#829e8e;stroke-width:1.5}.arrow{stroke:#617c6d;stroke-width:2;fill:none}.teal-line{stroke:#237a6c;stroke-width:3;fill:none}.orange-line{stroke:#b36e35;stroke-width:3;fill:none;stroke-dasharray:5 4}.patch-marker{fill:none;stroke:#efc65f;stroke-width:3}.im-code{background:#e7ecdf;border-left:3px solid #237a6c;padding:18px 14px;min-width:0}.im-label{font:15px 'IBM Plex Mono';color:#536d65;margin-bottom:16px}.im-code pre{font-size:16px!important;background:none!important;margin:0!important;padding:0!important;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.65!important}.im-code pre span{display:block;padding:4px 0}.im-code .active{background:#c5dccb}.im-caption{font-size:17px!important;line-height:1.35!important;color:#526d65;margin-top:20px!important}.im-slider{display:block;font-size:18px;margin-top:13px}.im-slider input{display:block;width:100%;accent-color:#237a6c}.im-slider input:focus-visible{outline:3px solid #b36e35;outline-offset:3px}
</style>
