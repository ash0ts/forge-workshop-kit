<script setup>
const props = defineProps({mode: {default: 'residual'}, reveal: {default: 2}})
const descriptions = {
  residual: 'Two observed image channels enter the CNN. It predicts one correction channel. Add the current image to produce a future forecast; a zero correction is persistence.',
  mask: 'Compare the predicted and observed image. Take absolute pixel errors, keep only the fixed disk mask, average within each image, then average images.',
  search: 'Hyperparameters change values in an existing program. Architecture comparison selects an existing implementation. A research agent changes model or training code; the same data and scorer test the result.',
  freeze: 'Choose code and trained weights using validation dates. Freeze both. Load those weights once on reserved February 13 and 14 inputs, then compare the predictions with observed futures.',
  weights: 'The language model research agent has fixed weights and writes code. The forecasting model trains new weights from that code and training observations. Validation results return to the agent.'
}
</script>
<template><svg viewBox="0 0 1120 360" role="img" :aria-label="descriptions[mode]">
<defs><marker id="solar-arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6" fill="none" stroke="#52776d" stroke-width="1.5"/></marker></defs>
<g v-if="mode==='residual'">
 <rect x="35" y="65" width="200" height="175" rx="5" fill="#dbe6e1"/><text x="135" y="105" text-anchor="middle">Two observations</text><text x="135" y="146" text-anchor="middle" class="mono">x[:, 0:1] · −60 min</text><text x="135" y="184" text-anchor="middle" class="mono">x[:, 1:2] · now</text><text x="135" y="218" text-anchor="middle" class="small" style="font-size:17px">batch × 2 × 64 × 64</text>
 <path d="M235 150H300" class="arrow"/><rect x="310" y="104" width="180" height="92" rx="5" fill="#163c43"/><text x="400" y="145" text-anchor="middle" class="white">Small CNN</text><text x="400" y="176" text-anchor="middle" class="small white">self.net(x)</text>
 <path d="M490 150H560" class="arrow"/><rect x="570" y="104" width="190" height="92" rx="5" fill="#f1ca70"/><text x="665" y="144" text-anchor="middle">{{reveal>=2?'Correction':'Whole forecast'}}</text><text x="665" y="177" text-anchor="middle" class="small">batch × 1 × 64 × 64</text>
 <g v-if="reveal>=2"><path d="M760 150H815" class="arrow"/><circle cx="845" cy="150" r="25" fill="#f6f2e7" stroke="#163c43" stroke-width="2"/><text x="845" y="160" text-anchor="middle" font-size="36">+</text><path d="M135 240V281H845V180" class="arrow"/><text x="490" y="271" text-anchor="middle" class="small">Copy the current image around the network</text><path d="M873 150H925" class="arrow"/><rect x="935" y="104" width="155" height="92" fill="#bad8cd" rx="5"/><text x="1012" y="144" text-anchor="middle">Forecast</text><text x="1012" y="176" text-anchor="middle" class="small">+60 minutes</text></g>
 <text x="560" y="337" text-anchor="middle" class="mono">{{reveal>=2?'return x[:, 1:2] + self.net(x)':'return self.net(x)'}}</text>
</g>
<g v-else-if="mode==='mask'">
 <g transform="translate(35 65)"><rect width="180" height="180" fill="#ecdfd3"/><circle cx="90" cy="90" r="68" fill="#cb8549"/><path d="M68 55L105 92L130 80" stroke="#f8dd97" stroke-width="17" fill="none"/><text x="90" y="220" text-anchor="middle">Pixel errors</text></g>
 <text x="250" y="170" font-size="40">×</text>
 <g transform="translate(295 65)"><rect width="180" height="180" fill="#294b50"/><circle cx="90" cy="90" r="68" fill="#fffaf0"/><text x="90" y="89" text-anchor="middle">1</text><text x="17" y="29" class="white small">0</text><text x="90" y="220" text-anchor="middle">Fixed disk mask</text></g>
 <path d="M495 150H565" class="arrow"/>
 <g transform="translate(585 65)"><rect width="180" height="180" fill="#294b50"/><circle cx="90" cy="90" r="68" fill="#cb8549"/><path d="M68 55L105 92L130 80" stroke="#f8dd97" stroke-width="17" fill="none"/><text x="90" y="220" text-anchor="middle">On-disk errors</text></g>
 <path d="M785 150H845" class="arrow"/><text x="960" y="127" text-anchor="middle">Sum ÷ disk pixels</text><text x="960" y="168" text-anchor="middle" class="small">One score per image</text><text x="960" y="211" text-anchor="middle" class="small">Then average images</text>
 <text x="560" y="337" text-anchor="middle" class="small">Illustration of the calculation. Off-disk changes contribute zero.</text>
</g>
<g v-else-if="mode==='search'">
 <g v-for="(row,i) in [['Hyperparameters','learning_rate = .003','Same program; different values'],['Architecture','architecture = residual','Choose an implementation'],['Agent-directed research','loss = abs(prediction − target)','Write and test different code']]" :key="i" :transform="`translate(25 ${35+i*104})`"><rect width="1070" height="83" rx="4" :fill="i===2?'#dbe6e1':'#ecebdf'"/><text x="22" y="49">{{row[0]}}</text><text x="365" y="35" class="mono">{{row[1]}}</text><text x="365" y="64" class="small">{{row[2]}}</text><text x="1035" y="49" text-anchor="end" class="small">{{i===2?'Agent proposes':'You configure'}}</text></g>
</g>
<g v-else-if="mode==='freeze'">
 <rect x="25" y="64" width="285" height="190" fill="#f1ca70" rx="5"/><text x="168" y="105" text-anchor="middle">Choose on validation</text><text x="168" y="148" text-anchor="middle" class="small">February 11–12</text><text x="168" y="187" text-anchor="middle" class="mono">candidate.py + weights.pt</text><text x="168" y="224" text-anchor="middle" class="small">Save the tested pair</text>
 <path d="M310 158H385" class="arrow"/><line x1="412" y1="35" x2="412" y2="283" stroke="#163c43" stroke-width="4"/><text x="412" y="322" text-anchor="middle" class="small">Freeze: no more selection</text>
 <path d="M432 158H505" class="arrow"/><rect x="520" y="64" width="250" height="190" fill="#c6d9e7" rx="5"/><text x="645" y="105" text-anchor="middle">Load, then predict</text><text x="645" y="148" text-anchor="middle" class="small">February 13–14</text><text x="645" y="187" text-anchor="middle" class="small">No weight updates</text><text x="645" y="224" text-anchor="middle" class="small">Same cases for all versions</text>
 <path d="M770 158H840" class="arrow"/><rect x="855" y="100" width="240" height="115" fill="#bad8cd" rx="5"/><text x="975" y="141" text-anchor="middle">Compare predictions</text><text x="975" y="181" text-anchor="middle" class="small">Error + actual images</text>
</g>
<g v-else-if="mode==='weights'">
 <rect x="40" y="65" width="315" height="180" fill="#163c43" rx="5"/><text x="197" y="106" text-anchor="middle" class="white">Research agent</text><text x="197" y="148" text-anchor="middle" class="white small">Fixed language-model weights</text><text x="197" y="193" text-anchor="middle" class="white small">Reads evidence, writes Python</text>
 <path d="M355 122H655" class="arrow"/><text x="505" y="100" text-anchor="middle" class="small">Reviewed code change</text>
 <rect x="675" y="65" width="395" height="180" fill="#bad8cd" rx="5"/><text x="872" y="106" text-anchor="middle">Forecasting experiment</text><text x="872" y="148" text-anchor="middle" class="small">Train small-network weights on earlier dates</text><text x="872" y="193" text-anchor="middle" class="small">Score predictions on validation dates</text>
 <path d="M675 220H410V272H197V250" class="arrow"/><text x="560" y="310" text-anchor="middle" class="small">Return the results, errors, and exact tested source</text>
</g>
</svg></template>
<style scoped>
svg{display:block;width:100%;height:355px;margin-top:20px}text{font:23px 'IBM Plex Sans',Arial;fill:#163c43}.small{font-size:19px}.mono{font:17px 'IBM Plex Mono',monospace}.white{fill:#f6f2e7}.arrow{fill:none;stroke:#52776d;stroke-width:2.5;marker-end:url(#solar-arrow)}
</style>
