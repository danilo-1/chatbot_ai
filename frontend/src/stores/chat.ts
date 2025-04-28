import { defineStore } from 'pinia'
import api from '@/services/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as Message[],
    userInput: '',
    isLoading: false,
    sessionId: '' as string,
    selectedModel: 'gpt-4o-mini' as string
  }),
  actions: {
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return

      const content = this.userInput
      this.messages.push({ role: 'user', content })
      this.userInput = ''
      this.isLoading = true

      try {
        const { data } = await api.post('/chat/', {
          session_id: this.sessionId || undefined,
          message: content,
          model: this.selectedModel
        })

        this.sessionId = data.session_id
        this.messages = data.history
      } catch (err) {
        console.error(err)
        this.messages.push({ role: 'assistant', content: 'Erro ao conectar com o servidor.' })
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchHistory() {
      if (!this.sessionId) return
      try {
        const { data } = await api.get(`/chat/history/${this.sessionId}`)
        this.messages = data.history
      } catch (err) {
        console.error(err)
      }
    },

    reset() {
      this.messages = []
      this.sessionId = ''
    }
  },
  persist: { key: 'fastchat-history', paths: ['messages'] }
})