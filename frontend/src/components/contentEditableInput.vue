<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  modelValue: string
  disabled?: boolean
  placeholder?: string
}>()
const emit = defineEmits(['update:modelValue', 'send'])

const el = ref<HTMLDivElement | null>(null)

const updateModel = () =>
  emit('update:modelValue', el.value?.innerText ?? '')

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    emit('send')
  }
}

/* mantém DOM ↔ state sincronizados */
watch(() => props.modelValue, v => {
  if (el.value && el.value.innerText !== v) el.value.innerText = v
})

onMounted(() => el.value!.innerText = props.modelValue)
</script>

<template>
  <div
    ref="el"
    class="chat-editor rounded-pill py-2 px-3"
    :class="{ disabled: props.disabled }"
    :contenteditable="!props.disabled"
    :data-placeholder="props.placeholder"
    @input="updateModel"
    @keydown="onKeydown"
  />
</template>

<style scoped>
.chat-editor {
  min-height: 38px; max-height: 300px;
  overflow-y: auto; outline: none;
  background: var(--bg-card); color: var(--txt-pri);
}

/* Placeholder para contenteditable */
.chat-editor[data-placeholder]:empty:before {
  content: attr(data-placeholder);
  color: var(--txt-sec);
  pointer-events: none;
}

/* desativa seleção quando desabilitado */
.chat-editor.disabled { opacity:.6; pointer-events:none; }
</style>