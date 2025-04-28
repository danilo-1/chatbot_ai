<template>
    <div :class="['p-3 rounded-3', baseCls]" :style="styleObj">
      <!-- Renderiza o markdown, se houver -->
      <div v-if="parsedMarkdown" v-html="parsedMarkdown"></div>
      <!-- Se houver HTML, renderiza o iframe (sempre visível) e o botão que controla a exibição do código -->
      <div v-if="htmlContent" class="mb-2">
        <iframe
          :srcdoc="htmlContent"
          class="html-frame mb-2 rounded-3"
          sandbox="allow-scripts allow-same-origin"
          style="width: 100%;"
          @load="resize"
        ></iframe>
        <button
          class="btn btn-sm btn-link"
          @click="toggleCode"
        >
          <i class="bi bi-code-slash"></i>
          {{ codeOpen ? 'Esconder código-fonte' : 'Mostrar código-fonte' }}
        </button>
        <div v-if="codeOpen" class="card mt-2">
          <pre class="p-2 code-block">{{ htmlContent }}</pre>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  import { marked } from 'marked'
  
  interface Message {
    content: string
    role: string
  }
  
  const props = defineProps<{ message: Message }>()
  
  // Funções utilitárias para extrair HTML e markdown
  const extractHtml = (t: string) =>
    (t.match(/<\!DOCTYPE html[\s\S]*?<\/html>/i) ||
      t.match(/<html[\s\S]*?<\/html>/i))?.[0] ?? ''
  const extractMarkdown = (t: string) =>
    t.replace(/<\!DOCTYPE html[\s\S]*?<\/html>/i, '')
     .replace(/<html[\s\S]*?<\/html>/i, '')
     .trim()
  
  // Controle de exibição do código-fonte
  const codeOpen = ref(false)
  const toggleCode = () => {
    codeOpen.value = !codeOpen.value
  }
  
  const resize = (e: Event) => {
    const frame = e.target as HTMLIFrameElement
    try {
      frame.style.height = frame.contentDocument?.body.scrollHeight + 50 + 'px'
    } catch (_) {}
  }
  
  const htmlContent = extractHtml(props.message.content)
  const markdownContent = extractMarkdown(props.message.content)
  
  const baseCls = computed(() =>
    props.message.role === 'user' ? 'bg-primary text-white' : 'bg-body-secondary'
  )
  const styleObj = { maxWidth: '90%' }
  const parsedMarkdown = computed(() =>
    markdownContent ? marked.parse(markdownContent) : ''
  )
  </script>
  
  <style scoped>
  /* Estilização aprimorada para blocos de código */
  .code-block {
    background-color: #2d2d2d;
    color: #ccc;
    font-family: 'Fira Code', Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    font-size: 0.9rem;
    overflow-x: auto;
    padding: 1rem;
    border-radius: 0.25rem;
    /* Opcional: adicionar uma sombra interna */
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
  }
  
  .card pre {
    margin: 0;
  }
  
  .html-frame {
    border: none;
  }
  </style>