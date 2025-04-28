import { defineStore } from 'pinia'
import api from '@/services/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export const useProcessCodeStore = defineStore('process', {
    state: () => ({
      code: '' as string,
      isLoading: false as boolean,
      processedCode: '' as string,
    }),
    actions: {
      async sendProcessCode() {
        if (!this.code.trim()) return
        this.isLoading = true
        try {
          const { data } = await api.post('/process/', { code: this.code })
          // Since `data` is a string, assign it to processedCode
          this.processedCode = data
        } catch (err: any) {
          console.error(err)
          this.processedCode = 'Error processing code: ' + err.message
        } finally {
          this.isLoading = false
        }
      },
    },
  })