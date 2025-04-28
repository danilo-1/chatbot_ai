<template>
    <div class="d-flex flex-column align-items-center justify-content-center h-100">
      <p class="mb-3 fs-5">Sugestões para começar uma conversa:</p>
      <div class="d-flex gap-2 flex-wrap justify-content-center">
        <button
          v-for="s in suggestions"
          :key="s"
          class="btn btn-outline-secondary btn-sm rounded-pill"
          @click="$emit('select', s)"
        >
          {{ s }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  const props = defineProps<{ suggestions: string[] }>()
  </script>
  
  <style scoped>
  /* Adicione estilos conforme necessário */
  </style>