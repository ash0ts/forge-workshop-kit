<script setup>
import { computed } from 'vue'
const props = defineProps({src:String,x:Number,y:Number,width:Number,height:Number,label:String,markers:{type:Array,default:()=>[]}})
const imageUrl = computed(() => import.meta.env.BASE_URL + props.src.replace(/^\//, ''))
</script>
<template><svg :viewBox="`${x-(markers.length?48:0)} ${y} ${width+(markers.length?48:0)} ${height}`" role="img" :aria-label="label" style="width:100%;border:1px solid #aab9ad;border-radius:6px;background:#17191c"><image :href="imageUrl" x="0" y="0" width="1280" height="720"/><rect v-if="markers.length" :x="x-48" :y="y" width="48" :height="height" fill="#17191c"/><g v-for="marker in markers" :key="marker.number"><path :d="`M${x-9} ${marker.y}H${x+5}`" stroke="#f1ca70" stroke-width="2"/><circle :cx="x-26" :cy="marker.y" r="16" fill="#f1ca70"/><text :x="x-26" :y="marker.y+6" text-anchor="middle" fill="#163c43" font-family="IBM Plex Sans" style="font-size:18px;font-weight:600">{{ marker.number }}</text></g></svg></template>
