<script setup>
import {useId} from 'vue'
const arrow=useId().replace(/:/g,'')
</script>
<template>
<svg class="mechanism" viewBox="0 0 1120 435" role="img" aria-label="Local MCP: the Python executor initializes a stdio server, lists onboarding tools and their schemas, calls provision_member with arguments, and receives the tool result. The server uses the same office simulator and writes account state to office.json. The returned observation enters the next model request.">
<defs><marker :id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#527b72"/></marker></defs>
<g font-family="IBM Plex Sans" fill="#163c43">
<text x="20" y="30" style="font-size:24px">Python executor</text><text x="600" y="30" style="font-size:24px">Local MCP server</text><text x="910" y="30" style="font-size:24px">Office simulator</text>
<path d="M120 55V405M700 55V405" stroke="#a2b3a6" stroke-width="2"/>
<path d="M120 91H691" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="410" y="78" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:22px">client.initialize()</text>
<path d="M120 151H691" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="410" y="138" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:22px">client.list_tools()</text>
<path d="M700 210H129" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="410" y="197" text-anchor="middle" style="font-size:21px">tool names + inputSchema</text>
<path d="M120 286H691" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="410" y="268" text-anchor="middle" font-family="IBM Plex Mono" style="font-size:20px">call_tool("provision_member", arguments)</text>
<path d="M706 286H906" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/>
<rect x="915" y="245" width="185" height="100" rx="8" fill="#f3e4b7"/><text x="1007" y="278" text-anchor="middle" style="font-size:22px">execute(…)</text><text x="1007" y="310" text-anchor="middle" style="font-size:19px">read / write state</text>
<path d="M915 342H700V365H129" fill="none" stroke="#527b72" stroke-width="3" :marker-end="`url(#${arrow})`"/><text x="410" y="353" text-anchor="middle" style="font-size:21px">JSON result → my_observation</text>
<text x="20" y="430" style="font-size:18px">A local subprocess communicates over stdio. office.json preserves the simulated state between calls.</text>
</g></svg>
</template>
