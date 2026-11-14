<script setup>
import { ref, computed } from 'vue'
import examples from '../data/recorded-review.json'
const selected=ref(0), reveal=ref(false)
const row=computed(()=>examples[selected.value])
function change(index){selected.value=index;reveal.value=false}
</script>
<template>
<div class="case-picker">
  <label>Recorded review example <select :value="selected" @change="change(Number($event.target.value))"><option v-for="(item,index) in examples" :value="index">{{ index+1 }} · {{ item.case_id }}</option></select></label>
  <div class="ticket"><small>Actual Banking77 request</small>{{ row.text }}</div>
  <div class="two-col"><div><h2>Classifier route</h2><code>{{ row.prediction }}</code><p class="aside">Probability {{ row.confidence.toFixed(3) }}. This is not calibrated certainty.</p></div><div><button @click="reveal=!reveal">{{reveal?'Hide':'Show'}} the published label</button><p v-if="reveal"><code>{{ row.target }}</code></p><p v-else class="aside">Decide which workflow you would choose first.</p></div></div>
  <p class="caption">Recorded classifier output; source label from the dataset. No attendee review has been inferred.</p>
</div>
</template>
<style scoped>
.case-picker label{display:block;font-size:18px;margin-bottom:20px}.case-picker select{padding:6px;background:#e4e9dc;border:1px solid #7f998c;max-width:770px}.case-picker button{background:#163c43;color:#fff;padding:12px 20px;border-radius:4px;font-size:20px}.case-picker button:focus-visible,.case-picker select:focus-visible{outline:3px solid #c17b40;outline-offset:3px}
</style>
