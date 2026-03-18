<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <h2 class="mb-3 text-lg font-semibold">答案与引文</h2>
    <div class="leading-7">
      <template v-if="segments.length">
        <span v-for="(segment, index) in segments" :key="index">
          <span v-if="segment.type === 'text'" class="whitespace-pre-wrap">{{ segment.value }}</span>
          <span v-else class="group relative mx-0.5 inline-flex cursor-help items-center rounded bg-cyan-500/10 px-1 text-cyan-300">
            {{ segment.value }}
            <span class="invisible absolute bottom-full left-1/2 z-10 mb-2 w-80 -translate-x-1/2 rounded-xl border border-slate-700 bg-slate-950 p-3 text-xs text-slate-200 opacity-0 shadow-lg transition group-hover:visible group-hover:opacity-100">
              <span class="mb-1 block font-semibold text-cyan-300">{{ citationMap[segment.id]?.source || '未知来源' }}</span>
              <span>{{ citationMap[segment.id]?.statement || '未找到对应事实。' }}</span>
            </span>
          </span>
        </span>
      </template>
      <span v-else class="whitespace-pre-wrap">等待提问…</span>
    </div>
    <div v-if="citations.length" class="mt-4 grid gap-3 border-t border-slate-800 pt-4 text-sm text-slate-300">
      <div v-for="citation in citations" :key="citation.id" class="rounded-xl bg-slate-800/80 p-3">
        <div class="font-medium text-cyan-300">[{{ citation.id }}] {{ citation.source }}</div>
        <div class="mt-1">{{ citation.statement }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  answer: { type: String, required: true },
  citations: { type: Array, required: true },
})

const citationMap = computed(() => Object.fromEntries(props.citations.map((item) => [String(item.id), item])))

const segments = computed(() => {
  if (!props.answer) return []
  const parts = []
  const pattern = /(\[(\d+)\])/g
  let lastIndex = 0
  let match
  while ((match = pattern.exec(props.answer)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', value: props.answer.slice(lastIndex, match.index) })
    }
    parts.push({ type: 'citation', value: match[1], id: match[2] })
    lastIndex = pattern.lastIndex
  }
  if (lastIndex < props.answer.length) {
    parts.push({ type: 'text', value: props.answer.slice(lastIndex) })
  }
  return parts
})
</script>
