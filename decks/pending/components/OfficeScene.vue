<script setup>
import {useId} from 'vue'
const floorId = useId().replace(/:/g, '')
defineProps({ mode: {default: 'employee'} })
</script>
<template>
<svg viewBox="0 0 680 450" role="img" :aria-label="mode === 'editor' ? 'Illustration of the Pending Inc office. An employee has a terminal and handbook; a process editor works at a separate desk.' : mode === 'blank' ? 'Illustration of the Pending Inc office. An employee has a terminal, with no handbook supplied.' : 'Illustration of the Pending Inc office. An employee has a terminal and handbook beside the desk.'" class="office-scene">
  <defs><pattern :id="floorId" width="28" height="28" patternUnits="userSpaceOnUse"><rect width="28" height="28" fill="#e7e0cf"/><path d="M28 0H0V28" fill="none" stroke="#cfc5b0"/></pattern></defs>
  <path d="M25 112H655V422H25Z" :fill="`url(#${floorId})`" stroke="#0d292e" stroke-width="8"/>
  <path d="M25 112V26H655V112" fill="#c2cdbd" stroke="#0d292e" stroke-width="8"/>
  <rect x="71" y="49" width="247" height="42" fill="#0d292e"/><text x="194" y="76" text-anchor="middle" fill="#fff3cb" font-family="monospace" style="font-size:18px">PENDING, INC.</text>
  <rect x="495" y="46" width="114" height="51" fill="#ebf4ef" stroke="#0d292e" stroke-width="5"/><path d="M552 46V97M495 72H609" stroke="#0d292e" stroke-width="4"/>
  <g shape-rendering="crispEdges">
    <rect x="78" y="229" width="218" height="27" fill="#af724c"/><rect x="86" y="256" width="14" height="75" fill="#684e40"/><rect x="275" y="256" width="14" height="75" fill="#684e40"/>
    <rect x="103" y="160" width="100" height="66" fill="#143c43"/><rect x="112" y="168" width="82" height="48" fill="#8ec1ac"/><path d="M122 181H171M122 195H182" stroke="#24584e" stroke-width="6"/><rect x="141" y="224" width="27" height="6" fill="#143c43"/>
    <rect x="229" y="196" width="30" height="32" fill="#fff4d0"/><path d="M259 202H267V218H259" fill="none" stroke="#fff4d0" stroke-width="7"/>
    <rect x="184" y="276" width="47" height="49" fill="#edb58e"/><rect x="179" y="270" width="52" height="16" fill="#24383d"/><rect x="179" y="286" width="12" height="25" fill="#24383d"/><rect x="216" y="294" width="6" height="6" fill="#24383d"/>
    <rect x="173" y="325" width="69" height="48" fill="#467c9d"/><rect x="188" y="333" width="9" height="14" fill="#fff4d0"/><rect x="182" y="373" width="17" height="28" fill="#24383d"/><rect x="216" y="373" width="17" height="28" fill="#24383d"/>
    <g v-if="mode !== 'blank'"><rect x="314" y="168" width="70" height="86" fill="#f2c65f"/><rect x="324" y="181" width="50" height="7" fill="#775e2a"/><rect x="324" y="198" width="40" height="5" fill="#775e2a"/><rect x="324" y="212" width="43" height="5" fill="#775e2a"/><rect x="324" y="227" width="33" height="5" fill="#775e2a"/></g>
    <g v-if="mode === 'editor'">
      <rect x="422" y="229" width="177" height="27" fill="#af724c"/><rect x="430" y="256" width="14" height="75" fill="#684e40"/><rect x="577" y="256" width="14" height="75" fill="#684e40"/><rect x="450" y="160" width="100" height="66" fill="#143c43"/><rect x="459" y="168" width="82" height="48" fill="#ecc765"/><rect x="495" y="276" width="47" height="49" fill="#c28c6e"/><rect x="491" y="270" width="53" height="18" fill="#24383d"/><rect x="485" y="325" width="69" height="48" fill="#b86443"/><rect x="494" y="373" width="17" height="28" fill="#24383d"/><rect x="527" y="373" width="17" height="28" fill="#24383d"/>
    </g>
    <g v-else><rect x="503" y="300" width="55" height="57" fill="#b86443"/><rect x="510" y="231" width="17" height="68" fill="#3c7f68"/><rect x="478" y="243" width="36" height="20" fill="#3c7f68"/><rect x="527" y="256" width="44" height="20" fill="#3c7f68"/></g>
  </g>
  <g v-if="mode === 'editor'"><path d="M310 300Q360 350 415 300" fill="none" stroke="#b86443" stroke-width="4" stroke-dasharray="8 6"/><text x="405" y="143" style="font-size:16px" fill="#143c43">PROCESS IMPROVEMENT</text></g>
</svg>
</template>
