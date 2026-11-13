<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 425" role="img" aria-label="Illustrative retry after a committed membership write. Repeating the same operation_id and arguments returns the saved receipt with replayed true and leaves one membership. Using a new operation_id creates another write and a duplicate membership. Reusing an existing operation_id with different arguments is rejected.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<rect x="20" y="15" width="1080" height="68" rx="9" fill="#f3e4b7"/><text x="40" y="44" style="font-size:23px">After the committed write: Fern has Alex’s membership.</text><text x="40" y="71" font-family="IBM Plex Mono" style="font-size:20px">operations["join-alex"] = {signature: same intended write, receipt: success}</text>
<text x="25" y="130" style="font-size:20px">If the caller retries…</text>
<rect x="20" y="151" width="330" height="88" rx="9" fill="#d9e6ef"/><text x="40" y="183" style="font-size:23px">Same ID + same arguments</text><text x="40" y="216" font-family="IBM Plex Mono" style="font-size:18px">operation_id: "join-alex"</text>
<path d="M356 195H457" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="465" y="151" width="340" height="88" rx="9" fill="#dce8df"/><text x="485" y="183" style="font-size:23px">Return the saved receipt</text><text x="485" y="216" font-family="IBM Plex Mono" style="font-size:21px">replayed: true</text>
<path d="M813 195H870" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="891" y="183" style="font-size:26px">1 membership</text><text x="891" y="216" style="font-size:20px">no second write</text>
<rect x="20" y="270" width="330" height="88" rx="9" fill="#edcdaa"/><text x="40" y="302" style="font-size:23px">New ID + same arguments</text><text x="40" y="335" font-family="IBM Plex Mono" style="font-size:18px">operation_id: "join-alex-2"</text>
<path d="M356 314H457" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="465" y="270" width="340" height="88" rx="9" fill="#edcdaa"/><text x="485" y="302" style="font-size:23px">Apply another write</text><text x="485" y="335" style="font-size:20px">new ID has no saved receipt</text>
<path d="M813 314H870" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="891" y="302" style="font-size:26px">2 memberships</text><text x="891" y="335" style="font-size:20px">duplicate effect</text>
<text x="22" y="405" style="font-size:18px">Illustrative simulator behavior. An existing ID with different arguments returns an error instead of applying the write.</text>
</g></svg>
</template>
