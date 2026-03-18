<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <h2 class="mb-3 text-lg font-semibold">回答</h2>
    <div class="whitespace-pre-wrap leading-7">{{ answer }}</div>
    <div v-if="citations.length" class="mt-4 space-y-2 border-t border-slate-800 pt-4 text-sm text-slate-300">
      <div v-for="citation in citations" :key="citation.id" class="rounded-xl bg-slate-800/80 p-3">
        <div class="font-medium">[{{ citation.id }}] {{ citation.source }}</div>
        <div>{{ citation.statement }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  answer: {
    type: String,
    required: true,
  },
  citations: {
    type: Array,
    required: true,
  },
})
</script>
