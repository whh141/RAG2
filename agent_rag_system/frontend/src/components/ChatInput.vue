<template>
  <form class="flex gap-3" @submit.prevent="submit">
    <input
      v-model="draft"
      class="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100 outline-none"
      placeholder="输入问题，例如：学校图书馆周末几点关门？"
    />
    <button class="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950">发送</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['submit'])
const draft = ref('')

const submit = () => {
  if (!draft.value.trim()) return
  emit('submit', draft.value)
  draft.value = ''
}
</script>
