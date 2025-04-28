import { ref, watchEffect } from 'vue'
import { useChatStore } from '@/stores/chat'
import api from '@/services/api'

export const useSuggestions = () => {
  const chat = useChatStore()
  // Sugestões como array de strings:
  const suggestions = ref<string[]>([])

  const fetchSuggestion = async () => {
    if (chat.messages.length === 0) {
      // Se não houver histórico, usa o endpoint de sugestões padrão (5 sugestões variadas)
      try {
        const { data } = await api.get('/default-suggestions')
        suggestions.value = data.suggestions
      } catch (err) {
        console.error(err)
        suggestions.value = [
          'Qual seu livro favorito?',
          'Você curte música? Qual estilo?',
          'Qual destino de viagem te atrai?',
          'Qual prato você recomenda experimentar?',
          'Que tecnologia você acha inovadora?'
        ]
      }
    } else {
      // Se houver histórico, utiliza o endpoint padrão de sugestões baseado no histórico
      try {
        const { data } = await api.post('/suggestion', { history: chat.messages })
        suggestions.value = data.suggestions
      } catch (err) {
        console.error(err)
        suggestions.value = ['Como posso ajudar hoje?']
      }
    }
  }

  // Sempre dispara a busca de sugestões quando o histórico muda
  watchEffect(() => {
    fetchSuggestion()
  })

  return suggestions
}