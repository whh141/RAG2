<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-100">
    <div class="mb-4 flex items-center justify-between">
      <h2 class="text-lg font-semibold">知识库管理</h2>
      <button class="rounded-lg bg-rose-500 px-3 py-2 text-sm font-semibold text-white" @click="$emit('clear')">
        清空并重新向量化
      </button>
    </div>
    <div class="rounded-xl border border-dashed border-slate-700 p-4">
      <input type="file" accept=".txt,.pdf" @change="pickFile" />
      <button class="mt-3 rounded-lg bg-cyan-500 px-3 py-2 text-sm font-semibold text-slate-950" :disabled="!file" @click="upload">
        上传并向量化
      </button>
      <div class="mt-3 text-sm text-slate-300">当前 ChromaDB chunk 数：{{ chunks }}</div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload', 'clear'])
defineProps({ chunks: { type: Number, required: true } })
const file = ref(null)

const pickFile = (event) => {
  file.value = event.target.files?.[0] || null
}

const upload = () => {
  if (!file.value) return
  emit('upload', file.value)
  file.value = null
}
</script>
