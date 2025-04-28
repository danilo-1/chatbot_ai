<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h3>Processar Código</h3>
        <div class="mb-3">
          <textarea v-model="code" class="form-control" rows="5" placeholder="Cole seu código aqui..."></textarea>
        </div>
        <button class="btn btn-primary mb-3" @click="sendProcessCode" :disabled="isLoading || !code.trim()">
          <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
          Enviar
        </button>
        <div v-if="processedCode" class="alert alert-secondary">
          <h4>Resultado do Processamento:</h4>
          <pre>{{ processedCode }}</pre>
        </div>
        <button class="btn btn-secondary" @click="close">Fechar</button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { storeToRefs } from 'pinia'
  import {useProcessCodeStore} from "@/stores/process_code"
  

  const processCodeStore = useProcessCodeStore()
  const { code, isLoading, processedCode } = storeToRefs(processCodeStore)
  const { sendProcessCode } = processCodeStore
  
  const emit = defineEmits(['close'])
  const close = () => {
    emit('close')
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  .modal-content {
    background: var(--bg‑card);
    padding: 1.5rem;
    border-radius: 0.5rem;
    width: 90%;
    max-width: 600px;
  }
  </style>