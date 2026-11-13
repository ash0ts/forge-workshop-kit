<script setup>
defineProps({level:{default:1}})
</script>
<template><svg style="width:100%;height:auto;max-height:400px" viewBox="0 0 1100 370" role="img" aria-label="A provisioning request changes account state before its response times out. A status read confirms access was granted.">
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="40" y="40" style="font-size:22px">Employee</text><text x="720" y="40" style="font-size:22px">Onboarding service</text>
<path d="M150 60V350M855 60V350" stroke="#a2b3a6" stroke-width="2"/>
<path d="M150 95H855" stroke="#4382a6" stroke-width="4"/><path d="M840 88L855 95L840 102" fill="none" stroke="#4382a6" stroke-width="4"/>
<text x="500" y="82" text-anchor="middle" style="font-size:23px">provision_member(Fern, Alex, member)</text>
<g v-if="level>=2"><rect x="670" y="116" width="400" height="44" rx="6" fill="#d9e8d9"/><text x="690" y="145" style="font-size:22px">Account now includes Alex.</text>
<path d="M855 193H150" stroke="#c17b40" stroke-width="3" stroke-dasharray="9 6"/><text x="500" y="182" text-anchor="middle" style="font-size:23px">The response times out.</text></g>
<g v-if="level>=3"><path d="M150 254H855" stroke="#4382a6" stroke-width="3"/><path d="M840 247L855 254L840 261" fill="none" stroke="#4382a6" stroke-width="3"/><text x="500" y="242" text-anchor="middle" style="font-size:23px">onboarding_status(Fern)</text>
<path d="M855 322H150" stroke="#237a6c" stroke-width="3"/><path d="M165 315L150 322L165 329" fill="none" stroke="#237a6c" stroke-width="3"/><text x="500" y="309" text-anchor="middle" style="font-size:23px">Completed. Access exists.</text></g>
</g></svg></template>
