<script setup>
import { computed } from 'vue'
const props = defineProps({src:String,x:Number,y:Number,width:Number,height:Number,label:String})
const imageUrl = computed(() => import.meta.env.BASE_URL + props.src.replace(/^\//, ''))
</script>
<template><svg :viewBox="`${x} ${y} ${width} ${height}`" role="img" :aria-label="label" style="width:100%;border:1px solid #aab9ad;border-radius:6px;background:#17191c"><image :href="imageUrl" x="0" y="0" width="1280" height="720"/></svg></template>
