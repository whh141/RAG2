<template>
  <main class="min-h-screen bg-slate-950 p-6 text-slate-100">
    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-6 lg:grid-cols-[1.2fr,0.8fr]">
      <section class="space-y-4">
        <header class="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <h1 class="text-2xl font-bold">Agentic RAG 全景演示</h1>
          <p class="mt-2 text-sm text-slate-300">知识库、智能路由、多源推理生成、白盒可视化验证。</p>
        </header>
        <AnswerDisplay :answer="answer" :citations="citations" />
        <ChatInput @submit="sendQuery" />
      </section>

      <section class="space-y-4">
        <CoTVisualizer :current-node="currentNode" :logs="logs" />
        <KnowledgeAdmin :chunks="chunkCount" @upload="uploadFile" @clear="clearKnowledge" />
      </section>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { http } from './api/http_client'
import { createChatSocket } from './api/ws_client'
import AnswerDisplay from './components/AnswerDisplay.vue'
import ChatInput from './components/ChatInput.vue'
import CoTVisualizer from './components/CoTVisualizer.vue'
import KnowledgeAdmin from './components/KnowledgeAdmin.vue'

const answer = ref('')
const citations = ref([])
const logs = ref([])
const currentNode = ref('')
const chunkCount = ref(0)
let socket

const loadStats = async () => {
  const { data } = await http.get('/api/knowledge/stats')
  chunkCount.value = data.chunks
}

const sendQuery = (query) => {
  answer.value = ''
  citations.value = []
  logs.value = []
  currentNode.value = 'intent_classifier'
  socket.send(JSON.stringify({ query }))
}

const uploadFile = async (file) => {
  const form = new FormData()
  form.append('file', file)
  const { data } = await http.post('/api/knowledge/upload', form)
  chunkCount.value = data.total_chunks
}

const clearKnowledge = async () => {
  await http.delete('/api/knowledge/clear')
  chunkCount.value = 0
}

onMounted(async () => {
  await loadStats()
  socket = createChatSocket((message) => {
    if (message.type === 'node_status') {
      currentNode.value = message.node
      logs.value.push({ node: message.node, data: message.data })
    }
    if (message.type === 'token_stream') {
      answer.value += message.data
    }
    if (message.type === 'final_answer') {
      answer.value = message.content
      citations.value = message.citations || []
      currentNode.value = 'generator'
    }
  })
})
</script>
