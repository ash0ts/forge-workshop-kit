<script setup>
import { computed, ref } from 'vue'
const props=defineProps({kind:String,step:{type:Number,default:1}})
const cutoff=ref(.7)
const fixture=[{score:.95,defect:false},{score:.9,defect:true},{score:.7,defect:true},{score:.4,defect:true},{score:.1,defect:false}]
const counts=computed(()=>({misses:fixture.filter(r=>r.defect&&r.score<cutoff.value).length,alarms:fixture.filter(r=>!r.defect&&r.score>=cutoff.value).length}))
const code={
 data:['photo = record["image"]','label = record["label"]','mask = record["mask"]','','# Labels supervise the classifier.','# Masks are displayed for inspection.','# Masks never become model features.'],
 encoder:['image = resize(rgb, (224, 224))','image = imagenet_normalize(image)','','# Frozen ResNet-18 outputs:','whole.shape == (N, 512)','patches.shape == (N, 14, 14, 64)'],
 patch:['errors = nearest_patch_errors(','    data, rows, reference',')','local = np.log1p(errors).reshape(','    len(rows), -1',')','return np.concatenate(','    [whole, local], axis=1',')'],
 threshold:['positives = np.sort(','    scores[target == 1]',')[::-1]','position = ceil(recall * len(positives)) - 1','threshold = positives[position]','','predicted_defect = score >= threshold'],
 ranking:['# Ranking quality over all cutoffs:','average_precision_score(y, scores)','','# Operating errors at one cutoff:','flagged = scores >= threshold','misses = sum((y == 1) & ~flagged)','false_alarms = sum((y == 0) & flagged)'],
 review:['distance = np.abs(scores - threshold)','order = np.argsort(distance)','active_rows = rows[order[:24]]','','random_rows = rng.choice(','    rows, 24, replace=False',')','# Reveal labels only after selection.'],
 train:['model = inspection.fit_classifier(','    data, fit_rows, method,','    build_features=build_features,','    C=0.03',')','values = inspection.score(','    data, validation_rows, model,','    build_features=build_features',')'],
 freeze:['save_classifier(path, model, threshold)','','# Save these together:','# normal patch bank + its case IDs','# feature function + normalization','# classifier coefficients','# threshold + validation decision','','# Reload before final prediction.']}
const active=computed(()=>({data:props.step===1?[0,1]:[2,4,5,6],encoder:props.step===1?[0,1,4]:[3,4,5],patch:props.step===1?[0,1,2]:[3,4,5,6,7,8],threshold:props.step===1?[0,1,2,3,4]:[6],ranking:props.step===1?[0,1]:[3,4,5,6],review:props.step===1?[0,1,2]:[4,5,6,7],train:props.step===1?[0,1,2,3,4]:[5,6,7,8],freeze:props.step===1?[0,2,3,4,5,6]:[8]}[props.kind]||[]))
</script>
<template>
<div class="walk-layout">
 <div class="walk-visual">
  <template v-if="kind==='data'">
   <div class="board-objects"><img src="/images/fit-defect.jpg" alt="Actual defective board from the VisA PCB1 fitting partition"/><div><h2>One board</h2><p>Input: photograph</p><p>Target: defective or normal</p><p v-if="step>1">Mask: annotated defect pixels</p></div></div>
   <div class="lane"><b>{{step===1?'Predict the board-level label':'Use the mask to inspect a prediction'}}</b><p>{{step===1?'This workshop decides which boards to flag. It does not train a segmentation model.':'The annotation helps a person locate the supplied defect. It is kept out of feature extraction and fitting.'}}</p></div>
  </template>
  <template v-else-if="kind==='encoder'">
   <div class="board-objects"><div class="gridded-board"><img src="/images/fit-defect.jpg" alt="PCB photograph with a schematic 14 by 14 feature-position grid"/><div v-if="step>1" class="patch-grid"><i v-for="i in 196" :key="i"/></div></div><div><h2>Frozen ResNet-18</h2><p>224 × 224 RGB input</p><p>512 whole-image values</p><p v-if="step>1">14 × 14 positions<br>64 values per position</p></div></div>
   <p>{{step===1?'The encoder already learned visual features on ImageNet. We train a small classifier on its outputs.':'Each feature position describes an overlapping receptive field. The grid is a location guide, not 196 independently classified image tiles.'}}</p>
  </template>
  <template v-else-if="kind==='patch'">
   <svg viewBox="0 0 640 300" role="img" :aria-label="step===1?'Compare a query patch with normal training patches at the same feature position. Use the closest distance.':'Flatten 196 log-transformed distances and append them to 512 whole-image features, producing 708 values per board.'">
    <template v-if="step===1">
     <rect x="20" y="40" width="180" height="90" rx="7"/><text x="36" y="76">Query position</text><text x="36" y="108" class="small">one 64-value vector</text>
     <path d="M210 85H290"/><rect x="305" y="15" width="310" height="160" rx="8"/><text x="325" y="50">Normal training bank</text><text x="325" y="87" class="small">same spatial position</text><text x="325" y="122" class="small">closest actual normal example</text><text x="325" y="157" class="small">exclude a board’s own match</text>
     <path d="M465 185V213"/><text x="75" y="253">One distance here; repeat at all 196 positions.</text>
    </template>
    <template v-else>
     <rect x="20" y="35" width="245" height="95" rx="8"/><text x="40" y="72">Whole image</text><text x="40" y="108">512 values</text><text x="285" y="91">+</text>
     <rect x="330" y="35" width="285" height="95" rx="8"/><text x="350" y="72">log1p(distance)</text><text x="350" y="108">14 × 14 = 196 values</text>
     <path d="M320 150V192"/><rect x="90" y="205" width="460" height="70" rx="8" class="accent"/><text x="122" y="249">One board → 708 classifier inputs</text>
    </template>
   </svg>
   <p>{{step===1?'Validation and test boards query the saved bank. They never join it. Distances are scaled using normal training features.':'log1p compresses large distances. Flatten preserves one row per board; axis=1 appends columns, not new training examples.'}}</p>
  </template>
  <template v-else-if="kind==='threshold'">
   <p class="walk-label">Public check fixture · three defects and two normal boards</p>
   <svg viewBox="0 0 640 180" role="img" aria-label="Five public fixture scores on a horizontal axis; a movable threshold changes which boards are flagged.">
    <line x1="35" y1="95" x2="605" y2="95"/><g v-for="(r,i) in fixture" :key="i"><circle :cx="35+r.score*570" cy="95" r="13" :class="r.defect?'accent':'muted'"/><text :x="35+r.score*570" :y="i===0?40:65" text-anchor="middle" class="small">{{r.score}}</text></g>
    <line :x1="35+cutoff*570" y1="15" :x2="35+cutoff*570" y2="130" class="cutoff"/><text x="35" y="166" class="small">normal = pale circle · defect = teal circle · flag at or above cutoff</text>
   </svg>
   <label class="slider-label">Cutoff {{cutoff.toFixed(2)}}<input aria-label="Inspection fixture threshold" type="range" min="0" max="1" step=".05" v-model.number="cutoff"/></label>
   <p><b>{{counts.misses}} missed defects · {{counts.alarms}} false alarms</b></p>
   <p>{{step===1?'At recall 2/3, choose 0.7: two of the three defects remain above the cutoff. This is exactly the notebook’s free check.':'In the real validation set, ceil(0.90 × 12) = 11 defects must be caught. That leaves at most one validation miss, not a guarantee for new boards.'}}</p>
  </template>
  <template v-else-if="kind==='ranking'">
   <p class="walk-label">Same public fixture, ranked from highest defect score</p>
   <div class="ranked-boards"><div v-for="(r,i) in fixture" :key="i" :class="r.defect?'is-defect':''"><b>{{i+1}}</b><span>{{r.defect?'defect':'normal'}}</span><strong>{{r.score}}</strong></div></div>
   <p v-if="step===1">Read from left to right. At each newly retrieved defect, precision is 1/2, 2/3, then 3/4. AP is their mean: <b>0.639</b>.</p>
   <p v-else>At cutoff 0.7: <b>one miss, one false alarm</b>. Moving the cutoff changes those counts. It does not change this ranking or its AP.</p>
   <p class="small">These five illustrative values come from check_threshold, not the recorded PCB1 evaluation. The test comparison ranks all 442 boards.</p>
  </template>
  <template v-else-if="kind==='review'">
   <svg viewBox="0 0 640 300" role="img" aria-label="The same parent detector selects two equal batches from 133 review boards, 24 by distance to threshold and 24 randomly. Labels are revealed after selection.">
    <rect x="90" y="10" width="460" height="60" rx="7"/><text x="115" y="48">Same detector · 133 review boards</text>
    <path d="M320 80V100H155V125M320 100H485V125"/>
    <rect x="15" y="135" width="280" height="90" rx="7" class="accent"/><text x="38" y="170">24 near the cutoff</text><text x="38" y="205" class="small">abs(score − threshold)</text>
    <rect x="345" y="135" width="280" height="90" rx="7" :class="step>1?'accent':''"/><text x="368" y="170">24 random boards</text><text x="368" y="205" class="small">same pool · seed 17</text>
    <text v-if="step>1" x="30" y="280">Reveal labels → fit both on 397 + 24 boards</text>
   </svg>
   <p>{{step===1?'Choose using scores, without opening labels. Close to the cutoff means uncertain under this detector, not necessarily the most valuable label.':'The equal-budget random branch tests whether the selection rule adds value beyond simply acquiring more labels.'}}</p>
  </template>
  <template v-else-if="kind==='train'">
   <div class="lane"><b>Fit the classifier</b><p>397 fitting boards + your feature function</p><small>C = 0.03 · class-balanced logistic classifier</small></div>
   <div class="lane" :class="{faded:step<2}"><b>Evaluate validation predictions</b><p>132 different boards + the same feature function</p><small>Select a threshold; record AP, misses, and false alarms.</small></div>
   <p>{{step===1?'The training operation produces a model. Saving it and exporting its trace are separate operations.':'In Agent Lens, match the method and training count to the returned validation metrics. A tool span can describe CPU training without an LLM call.'}}</p>
  </template>
  <template v-else-if="kind==='freeze'">
   <div class="bundle"><b>Selected detector</b><p>Normal patch bank + training IDs</p><p>Feature source + scaling values</p><p>Classifier coefficients + threshold</p></div>
   <div v-if="step>1" class="lane"><b>Reload → score the same board</b><p>Compare the new score with its saved value.</p><small>Registry can name this artifact. It does not deploy this classifier.</small></div>
   <p v-else>The coefficients alone cannot reproduce the prediction. Each earlier transformation belongs to the version you freeze.</p>
  </template>
 </div>
 <div class="walk-code"><span class="walk-label">Relevant implementation</span><pre><template v-for="(line,i) in code[kind]" :key="i"><span :class="{active:active.includes(i)}">{{line||' '}}</span></template></pre></div>
</div>
</template>
