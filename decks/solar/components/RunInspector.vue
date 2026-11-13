<script setup>
import {ref} from 'vue'
import rows from '../data/recorded-runs.json'
const props=defineProps({revealed:Boolean})
const reveal=ref(props.revealed)
</script>
<template><div class="run-inspector"><p class="caption">Recorded GOES rehearsal. Both models remained worse than persistence.</p><table class="clean-table"><thead><tr><th>Experiment</th><th>Validation error ↓</th><th>Active settings</th></tr></thead><tbody><tr v-for="row in rows" :key="row.id"><td><a :href="row.run_url" target="_blank" rel="noopener">{{row.name}} ↗</a></td><td>{{row.validation_error.toFixed(6)}}</td><td v-if="reveal">{{row.config.architecture}}, width {{row.config.width}}, learning rate {{row.config.learning_rate}}</td><td v-else>Hidden for this illustration</td></tr></tbody></table><button @click="reveal=!reveal" :aria-expanded="reveal">{{reveal?'Hide settings':'Show active settings'}}</button><div class="run-explanation" aria-live="polite">{{reveal?'Same source, dates, seed, 60-step budget, and batch size. The active learning rate differs. Neither score tells you whether training had converged.':'What can you conclude from the score alone? Identify what you need before recommending either run.'}}</div></div></template>
<style scoped>button{margin:24px 0 17px;background:#163c43;color:#f6f2e7;padding:12px 20px;font:22px 'IBM Plex Sans';border:none;border-radius:4px;cursor:pointer}button:focus-visible{outline:4px solid #f1ca70;outline-offset:3px}.run-explanation{font-size:24px;line-height:1.45;min-height:84px}.caption{font-size:18px}</style>
