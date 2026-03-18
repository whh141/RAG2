<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <h2 class="mb-3 text-lg font-semibold">白盒化流程</h2>
    <div class="grid grid-cols-1 gap-3">
      <div
        v-for="node in nodes"
        :key="node"
        :class="[
          'rounded-xl border px-4 py-3 transition',
          currentNode === node ? 'border-cyan-400 bg-cyan-500/10' : 'border-slate-700 bg-slate-950/60'
        ]"
      >
        {{ node }}
      </div>
    </div>
    <div class="mt-5 space-y-2 text-sm text-slate-300">
      <div v-for="(log, index) in logs" :key="index" class="rounded-lg bg-slate-950/70 p-3">
        <span class="font-semibold text-cyan-300">{{ log.node }}</span>
        <span class="ml-2">{{ log.data }}</span>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  currentNode: {
    type: String,
    default: '',
  },
  logs: {
    type: Array,
    required: true,
  },
})

const nodes = ['intent_classifier', 'retriever_local', 'retriever_web', 'reranker', 'compressor', 'generator']
</script>
