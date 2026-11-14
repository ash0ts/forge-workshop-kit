<script setup>
defineProps({level:{default:1}})
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 410" role="img" aria-label="Illustrative evaluation: an agent claims a full refund but the account has only a 100-cent refund instead of 4900 cents. The development scorer fails. A judge response can be valid JSON and still incorrectly claim completion; inspect its reason against recorded work. An unavailable judge remains missing.">
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="18" y="25" width="520" height="112" rx="7" fill="#e4eadd"/>
<text x="40" y="64" style="font-size:23px">Agent reply: “The full $49 is refunded.”</text>
<text x="40" y="105" style="font-size:21px">Observed account: one $1 refund</text>
<rect x="566" y="25" width="533" height="112" rx="7" fill="#f3e4b7"/>
<text x="587" y="64" style="font-size:23px">State check: 100 != 4900 cents</text>
<text x="587" y="105" style="font-size:21px">The partial refund fails the known fixture.</text>
<g v-if="level>=2">
<text x="18" y="186" style="font-size:22px">Three questions about the explanation judge</text>
<text x="23" y="239" style="font-size:21px">1. Did it return?</text><text x="340" y="239" style="font-size:21px">If unavailable, leave its score missing.</text>
<text x="23" y="285" style="font-size:21px">2. Is its answer valid?</text><text x="340" y="285" style="font-size:21px">Booleans + a nonempty reason pass the schema.</text>
<text x="23" y="331" style="font-size:21px">3. Is it right?</text><text x="340" y="331" style="font-size:21px">A “complete: true” answer would be wrong here.</text>
</g>
<text x="18" y="395" style="font-size:18px">Teaching example from the public partial-refund fixture. The quoted reply and judge answer are illustrative, not recorded judgments.</text>
</g></svg>
</template>
