<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <h2 class="mb-3 text-lg font-semibold">答案与引文</h2>
    <div class="whitespace-pre-wrap leading-7">{{ answer || '等待提问…' }}</div>
    <div v-if="citations.length" class="mt-4 grid gap-3 border-t border-slate-800 pt-4 text-sm text-slate-300">
      <div v-for="citation in citations" :key="citation.id" class="rounded-xl bg-slate-800/80 p-3">
        <div class="font-medium text-cyan-300">[{{ citation.id }}] {{ citation.source }}</div>
        <div class="mt-1">{{ citation.statement }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  answer: { type: String, required: true },
  citations: { type: Array, required: true },
})
</script>
