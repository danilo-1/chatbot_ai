<template>
  <div class="chat-container">
    <!-- Header fixo -->
    <header class="chat-header">
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container-fluid">
          <span class="navbar-brand fw-bold">
            <i class="bi bi-robot"></i> FastChat
          </span>
          <div class="d-flex align-items-center gap-1 ms-auto">
            <div class="input-group">
              <span class="input-group-text bg-primary text-white">Modelo</span>
              <select v-model="selectedModel" class="form-select" id="inputGroupSelect01">
                <option selected value="gpt-4o-mini">GPT‑4o Mini</option>
                <option value="gpt-4.1">GPT‑4.1</option>
                <option value="o4-mini">o4 Mini</option>
              </select>
            </div>
            <!-- Botão com tooltip -->
            <button type="button" class="btn btn-sm btn-outline-light"
              @click="newChatConfirm"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Iniciar um novo chat">
              <i class="bi bi-file-earmark-plus"></i>
            </button>
            <router-link to="/" class="btn btn-sm btn-outline-light"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            data-bs-title="Voltar para tela principal">
              <i class="bi bi-house-fill"></i></router-link>
            <button @click="toggle" class="btn btn-sm btn-outline-light"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Alternar tema">
              <i :class="theme==='dark' ? 'bi-sun' : 'bi-moon-stars'"></i>
            </button>
          </div>
        </div>
      </nav>
    </header>

    <!-- Histórico rolável -->
    <main class="chat-history" ref="chatBody">
      <transition-group name="fade" tag="div">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="d-flex mb-3"
          :class="{ 'justify-content-end': msg.role==='user' }">
          <div v-if="msg.role==='assistant'" class="flex-shrink-0 me-2">
            <span class="avatar bg-primary text-white"><i class="bi bi-robot"></i></span>
          </div>
          <!-- use o componente BubbleComponent -->
          <BubbleComponent :message="msg" />
          <div v-if="msg.role==='user'" class="flex-shrink-0 ms-2">
            <span class="avatar bg-secondary text-white"><i class="bi bi-person"></i></span>
          </div>
        </div>
      </transition-group>
      <div v-if="isLoading" class="text-center my-4">
        <div class="spinner-border text-primary" role="status" />
      </div>
    </main>

    <!-- Footer fixo -->
    <footer class="chat-footer">
      <form @submit.prevent="sendMessage" class="d-flex gap-2">
        <ContentEditableInput
          v-model="userInput"
          :disabled="isLoading"
          class="form-control flex-grow-1"
          placeholder="Digite sua mensagem…"
          @send="sendMessage"
        />
        <button class="btn btn-primary d-flex align-items-center gap-1" :disabled="isLoading || !userInput.trim()">
          <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
          <i v-else class="bi bi-send-fill"></i>
        </button>
      </form>
    </footer>
    <button class="btn btn-info position-fixed" style="bottom: 80px; right: 20px;" @click="showProcessModal = true">
      Processar Código
    </button>

    <!-- Modal for processing code -->
    <ProcessModal v-if="showProcessModal" @close="showProcessModal = false" />
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onBeforeUnmount, ref, defineComponent, h } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import { marked } from 'marked'
import { useTheme } from '@/composables/useTheme'
import ContentEditableInput from '@/components/ContentEditableInput.vue'
import BubbleComponent from '@/components/BubbleComponent.vue'
import ProcessModal from '@/components/ProcessModal.vue'
import { Tooltip } from 'bootstrap'

const chatStore = useChatStore()
const { messages, userInput, isLoading, selectedModel } = storeToRefs(chatStore)
const { sendMessage } = chatStore
const { theme, toggle } = useTheme()
const chatBody = ref<HTMLElement | null>(null)
const showProcessModal = ref(false)

// Armazena as instâncias dos tooltips
const tooltips = ref<Tooltip[]>([])

function newChatConfirm () {
  if (confirm('Iniciar um novo chat? O histórico atual será apagado.')) {
    chatStore.reset()
  }
}

onMounted(() => {
  // Inicializa os tooltips do Bootstrap e armazena as instâncias
  const tooltipElements = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipElements.forEach(el => tooltips.value.push(new Tooltip(el)))
})

onBeforeUnmount(() => {
  // Desfaz todos os tooltips para evitar persistência na DOM
  tooltips.value.forEach(tt => tt.dispose())
})

onMounted(async () => {
  await nextTick()
  chatBody.value?.scrollTo({ top: chatBody.value.scrollHeight, behavior: 'smooth' })
})
</script>

<style scoped>
.chat-container {
  position: relative;
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.chat-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}
.chat-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 0.5rem;
}
.chat-history {
  flex: 1;
  overflow-y: auto;
  margin-top: 70px;
  margin-bottom: 70px;
  padding: 1rem;
}
.avatar {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.1rem;
}
</style>