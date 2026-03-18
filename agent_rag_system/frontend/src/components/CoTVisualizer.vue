<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <div class="mb-3 flex items-center justify-between">
      <h2 class="text-lg font-semibold">白盒化流程</h2>
      <span class="rounded-full bg-cyan-500/10 px-3 py-1 text-xs text-cyan-300">{{ currentNode || 'idle' }}</span>
    </div>
    <div class="grid grid-cols-2 gap-3">
      <div
        v-for="node in nodes"
        :key="node.key"
        :class="[
          'rounded-xl border px-4 py-3 transition',
          currentNode === node.key ? 'border-cyan-400 bg-cyan-500/10' : 'border-slate-700 bg-slate-950/60'
        ]"
      >
        <div class="font-medium">{{ node.label }}</div>
        <div class="mt-1 text-xs text-slate-400">{{ node.desc }}</div>
      </div>
    </div>
    <div class="mt-5 space-y-3 text-sm text-slate-300">
      <div v-for="(log, index) in logs" :key="index" class="rounded-lg bg-slate-950/70 p-3">
        <div class="font-semibold text-cyan-300">{{ log.node }}</div>
        <div class="mt-1">{{ log.summary }}</div>
        <pre v-if="log.details" class="mt-2 overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs text-slate-300">{{ log.details }}</pre>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  currentNode: { type: String, default: '' },
  logs: { type: Array, required: true },
})

const nodes = [
  { key: 'intent_classifier', label: '意图识别', desc: 'local / web / hybrid' },
  { key: 'retriever_local', label: '本地检索', desc: 'ChromaDB 召回' },
  { key: 'retriever_web', label: '外部检索', desc: 'Tavily 搜索' },
  { key: 'reranker', label: '交叉熵重排', desc: 'Cross-Encoder' },
  { key: 'compressor', label: '事实压缩', desc: '提炼最小事实集' },
  { key: 'generator', label: '最终生成', desc: '答案 + [n] 引文' },
]
</script>
