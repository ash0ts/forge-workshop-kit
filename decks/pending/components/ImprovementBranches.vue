<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
defineProps({level:{default:1}})
</script>
<template><svg style="width:100%;height:auto;max-height:400px" viewBox="0 0 1120 390" role="img" aria-label="A tested parent branches into two proposed edits. Test both, review their evidence, decide which files to keep, test the chosen version and carry its lesson into another round.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43" style="font-size:22px">
<rect x="15" y="160" width="140" height="62" rx="8" fill="#dbe1d9"/><text x="85" y="185" text-anchor="middle">Parent files</text><text x="85" y="210" text-anchor="middle" style="font-size:17px">already tested</text>
<g v-if="level>=1"><path d="M155 191C185 191 185 70 235 70M155 191C185 191 185 300 235 300" fill="none" stroke="#527b72" stroke-width="3"/>
<rect x="235" y="38" width="175" height="66" rx="8" fill="#c7dde9"/><text x="322" y="66" text-anchor="middle">Candidate A</text><text x="322" y="92" text-anchor="middle" style="font-size:17px">review its diff</text>
<rect x="235" y="268" width="175" height="66" rx="8" fill="#edcdaa"/><text x="322" y="295" text-anchor="middle">Candidate B</text><text x="322" y="321" text-anchor="middle" style="font-size:17px">review its diff</text></g>
<g v-if="level>=2"><path d="M410 70H450M410 300H450" stroke="#527b72" stroke-width="3"/><circle cx="475" cy="70" r="18" fill="#4382a6"/><circle cx="475" cy="300" r="18" fill="#c17b40"/><text x="475" y="122" text-anchor="middle">Test A</text><text x="475" y="350" text-anchor="middle">Test B</text></g>
<g v-if="level>=3"><path d="M495 70C545 70 530 172 590 172M495 300C545 300 530 210 590 210" fill="none" stroke="#7d968b" stroke-width="3" stroke-dasharray="7 5"/>
<text x="540" y="30" style="font-size:17px">read test runs</text><rect x="590" y="143" width="190" height="98" rx="8" fill="#f1ca70"/><text x="685" y="172" text-anchor="middle">Compose decision</text><text x="685" y="200" text-anchor="middle" style="font-size:18px">select · combine</text><text x="685" y="225" text-anchor="middle" style="font-size:18px">or retain the parent</text></g>
<g v-if="level>=4"><path d="M780 192H832" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><circle cx="858" cy="192" r="18" fill="#163c43"/><text x="860" y="137" text-anchor="middle">Test chosen files</text><text x="860" y="243" text-anchor="middle" style="font-size:18px">verify selected files</text></g>
<g v-if="level>=5"><path d="M878 192C930 192 920 70 985 70M878 192C930 192 920 300 985 300" fill="none" stroke="#527b72" stroke-width="3"/><rect x="985" y="38" width="115" height="64" rx="8" fill="#d7e5db"/><text x="1042" y="65" text-anchor="middle">Next case</text><text x="1042" y="90" text-anchor="middle" style="font-size:17px">repeat</text><rect x="985" y="268" width="115" height="64" rx="8" fill="#ede3c7"/><text x="1042" y="295" text-anchor="middle">Save lesson</text><text x="1042" y="321" text-anchor="middle" style="font-size:17px">+ limits</text></g>
</g></svg></template>
