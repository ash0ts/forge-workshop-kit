<script setup>
import {useId} from 'vue'
const markerId = useId().replace(/:/g, '')
defineProps({ level: {default: 0}, active: {default: ''} })
</script>
<template>
<svg viewBox="0 0 1120 400" role="img" aria-label="An employee agent uses a fixed model. Instructions, loaded skills, tool definitions and its control loop form the editable harness.">
  <defs><marker :id="markerId" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#3d6568"/></marker></defs>
  <rect x="25" y="40" width="730" height="320" rx="20" fill="#f0ecdf" stroke="#899e97" stroke-width="2" stroke-dasharray="8 6"/>
  <text x="50" y="73" class="diagram-label">HARNESS · files + tools + control flow</text>
  <rect x="310" y="155" width="210" height="88" rx="10" fill="#163c43"/><text x="415" y="193" text-anchor="middle" fill="#fff" style="font-size:27px">Employee agent</text><text x="415" y="220" text-anchor="middle" fill="#b9d1ca" style="font-size:18px">chooses the next action</text>
  <rect x="860" y="155" width="225" height="88" rx="10" fill="#dbe6e1" stroke="#527b72" stroke-width="2"/><text x="972" y="191" text-anchor="middle" fill="#163c43" style="font-size:27px">Fixed model</text><text x="972" y="221" text-anchor="middle" fill="#52746a" style="font-size:18px">weights do not change</text>
  <path d="M520 199H852" stroke="#3d6568" stroke-width="3" :marker-end="`url(#${markerId})`"/><text x="790" y="179" text-anchor="middle" style="font-size:17px" fill="#3d6568">request</text>
  <g v-if="level >= 1"><rect x="59" y="106" width="184" height="70" rx="7" fill="#f1ca70"/><text x="151" y="135" text-anchor="middle" style="font-size:22px">instructions.md</text><text x="151" y="160" text-anchor="middle" style="font-size:17px">task rules + limits</text><path d="M243 144Q275 144 304 175" fill="none" stroke="#3d6568" stroke-width="3" :marker-end="`url(#${markerId})`"/></g>
  <g v-if="level >= 2"><rect x="59" y="230" width="184" height="70" rx="7" fill="#f1ca70"/><text x="151" y="260" text-anchor="middle" style="font-size:22px">verification skill</text><text x="151" y="285" text-anchor="middle" style="font-size:17px">must be loaded</text><path d="M243 265Q276 265 304 230" fill="none" stroke="#3d6568" stroke-width="3" :marker-end="`url(#${markerId})`"/></g>
  <g v-if="level >= 3"><rect x="550" y="86" width="177" height="64" rx="7" fill="#bad8cd"/><text x="638" y="115" text-anchor="middle" style="font-size:22px">Python tool</text><text x="638" y="139" text-anchor="middle" style="font-size:17px">name + input schema</text><path d="M550 119Q520 119 500 151" fill="none" stroke="#3d6568" stroke-width="3" :marker-end="`url(#${markerId})`"/></g>
  <g v-if="level >= 4"><rect x="550" y="258" width="177" height="64" rx="7" fill="#c6d9e7"/><text x="638" y="287" text-anchor="middle" style="font-size:22px">Control loop</text><text x="638" y="311" text-anchor="middle" style="font-size:17px">act → observe → repeat</text><path d="M550 289Q521 289 500 248" fill="none" stroke="#3d6568" stroke-width="3" :marker-end="`url(#${markerId})`"/></g>
  <text v-if="level === 0" x="75" y="325" fill="#64736b" style="font-size:22px">Management has not filled this in yet.</text>
</svg>
</template>
