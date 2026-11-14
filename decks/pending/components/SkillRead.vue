<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template><svg class="mechanism" viewBox="0 0 1120 400" role="img" aria-label="Saving verify-operation makes its name available in the system prompt. A successful read_skill call returns its text. The observation function must include that result in the next request. Inspect recorded reads and requests; if no read exists, do not claim the skill influenced this run.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g fill="#163c43" font-family="IBM Plex Sans">
<rect x="10" y="35" width="330" height="150" rx="9" fill="#dce8df"/><text x="30" y="70" style="font-size:26px">1 · Save the skill file</text><text x="30" y="108" style="font-size:20px" font-family="IBM Plex Mono">skills/verify-operation.md</text><text x="30" y="146" style="font-size:21px">Only its name enters the prompt.</text>
<path d="M350 107H385" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="395" y="35" width="330" height="150" rx="9" fill="#f1ca70"/><text x="415" y="70" style="font-size:26px">2 · Model requests it</text><text x="415" y="108" style="font-size:21px" font-family="IBM Plex Mono">read_skill</text><text x="415" y="143" style="font-size:20px" font-family="IBM Plex Mono">name: verify-operation</text>
<path d="M735 107H770" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="780" y="35" width="330" height="150" rx="9" fill="#d9e6ef"/><text x="800" y="70" style="font-size:26px">3 · Return the text</text><text x="800" y="108" style="font-size:20px">Append it as a tool observation.</text><text x="800" y="146" style="font-size:20px">Inspect the next model request.</text>
<text x="20" y="245" style="font-size:27px">A saved file alone does not show that the model used it.</text>
<text x="20" y="290" style="font-size:22px">Notebook step 5 shows the recorded read, returned skill, and matching request.</text>
<text x="20" y="330" style="font-size:22px">Then compare later tools: did the employee follow the procedure?</text>
<text x="20" y="380" style="font-size:18px">Illustrated mechanism. The notebook reads your saved events; it reports explicitly when no successful skill read exists.</text>
</g></svg></template>
