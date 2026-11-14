<script setup>
import { computed } from 'vue'
const props = defineProps({kind: {type:String, default:'mapping'}, step: {type:Number, default:1}})
const incorrect = computed(() => props.step === 2)
const classes = ['Card arrival', 'Card not working', 'Unknown cash withdrawal']
const labels = computed(() => incorrect.value ? [classes[1], classes[2], classes[0]] : classes)
const lines = computed(() => props.kind === 'mapping' ? [
  'p = model.predict_proba(requests)',
  'names = list(model.classes_)',
  ...(incorrect.value ? ['names = names[1:] + names[:1]', '# Deliberate release defect'] : ['# Keep the saved column order']),
  'column = p.argmax(axis=1)',
  'intent = names[column[0]]',
] : props.kind === 'checks' ? [
  'expected = list(model_classes)',
  'checks = {',
  '  "label_set":',
  '      set(loaded) == set(expected),',
  '  "label_order":',
  '      loaded == expected,',
  '}',
  '# Run prediction parity separately.',
] : [
  '# The notebook saves the exact version.',
  'artifact = "entity/project/router:v3"',
  'files = reproduce(artifact, restore_dir)',
  '# Read saved files; do not fit again.',
  'result = predict_saved_release(files)',
])
</script>
<template>
<div class="walk-layout release-walk">
 <div class="walk-visual">
  <template v-if="kind === 'mapping'">
   <span class="walk-label">ILLUSTRATIVE VALUES · THREE OF 77 COLUMNS</span>
   <div class="walk-request">“My card is here, but it won’t work.”</div>
   <svg viewBox="0 0 640 290" role="img" :aria-label="incorrect ? 'The same probabilities now point to rotated labels. The highest column incorrectly becomes unknown cash withdrawal.' : 'The highest probability is in column one. Reading the matching saved label returns card not working.'">
    <text x="12" y="25" class="label">Column</text><text x="120" y="25" class="label">Probability</text><text x="297" y="25" class="label">{{ incorrect ? 'Rotated labels: wrong' : 'Saved labels: correct' }}</text>
    <g v-for="(value, i) in ['0.08','0.84','0.08']" :key="i">
     <rect x="10" :y="43+i*68" width="235" height="54" rx="5" :class="i===1 ? 'accent' : ''"/>
     <text x="34" :y="78+i*68">{{i}}</text><text x="134" :y="78+i*68">{{value}}</text>
     <path :d="`M250 ${70+i*68}H282`"/>
     <rect x="290" :y="43+i*68" width="335" height="54" rx="5" :class="i===1 ? (incorrect ? 'fault' : 'accent') : ''"/>
     <text x="305" :y="78+i*68" class="small">{{labels[i]}}</text>
    </g>
    <text x="12" y="277" class="label">Confidence stays 0.84. {{incorrect ? 'The destination changes.' : 'The destination matches column 1.'}}</text>
   </svg>
  </template>
  <template v-else-if="kind === 'checks'">
   <span class="walk-label">CHECK THE CONTRACT, THEN THE PREDICTIONS</span>
   <svg viewBox="0 0 640 320" role="img" aria-label="Illustrative three-column release contract: both versions contain the same labels, but rotated column order fails. Restoring the order permits a separate prediction-parity check.">
    <text x="20" y="32" class="small">Saved probability columns</text><text x="358" y="32" class="small">{{step>2?'Repaired label order':'Rotated label order'}}</text>
    <g v-for="(label,i) in ['Arrival','Not working','Withdrawal']" :key="label">
     <rect x="20" :y="55+i*61" width="225" height="44" rx="5"/><text x="35" :y="84+i*61" class="small">{{i}} · {{label}}</text>
     <path :d="`M255 ${77+i*61}H345`" :style="{stroke:step>2?'#237a6c':'#b57139'}"/>
     <rect x="355" :y="55+i*61" width="265" height="44" rx="5" :class="step>2?'accent':'fault'"/><text x="370" :y="84+i*61" class="small">{{i}} · {{step>2?label:['Not working','Withdrawal','Arrival'][i]}}</text>
    </g>
    <text x="20" y="275" class="small">Same set: yes. {{step>2?'Same order: yes.':'Same order: no.'}}</text><text x="20" y="308" class="small">{{step>2?'Now compare predictions on the fixed 77-case batch.':'Set equality cannot detect the changed destinations.'}}</text>
   </svg>
   <p class="small">Prediction parity checks reproduction. It does not prove the classifier routes every request correctly.</p>
  </template>
  <template v-else>
   <span class="walk-label">LOAD THE FILES THAT PRODUCED THE RESULT</span>
   <div class="bundle"><b>Exact artifact version</b><div class="release-files"><span>Classifier</span><span>Feature recipe</span><span>Intent order</span><span>Review policy</span><span>Code + checks</span><span>Frozen case IDs</span></div></div>
   <svg viewBox="0 0 640 145" role="img" aria-label="Load the exact artifact version into a fresh folder and predict the fixed request batch without fitting again."><path d="M320 0V35"/><rect x="60" y="40" width="520" height="70" rx="7" class="accent"/><text x="80" y="71">Reload → predict → compare</text><text x="80" y="98" class="small">No training or model request</text></svg>
   <p class="small">The artifact name shown in code is illustrative. Use the exact version returned by your notebook.</p>
  </template>
 </div>
 <div class="walk-code"><span class="walk-label">{{ kind === 'bundle' ? 'ABBREVIATED RELEASE SEQUENCE' : 'CODE BEHIND THE CHANGE' }}</span><pre><span v-for="(line,i) in lines" :key="i" :class="{active:kind==='mapping' ? (incorrect ? i===2 : i===1) : kind==='checks' ? (step===1 ? i===2||i===3 : step===2 ? i===4||i===5 : i===7) : i===1||i===2}">{{line || ' '}}</span></pre></div>
</div>
</template>
